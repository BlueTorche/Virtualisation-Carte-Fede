import argon2
from flask_apispec import MethodResource
from flask import render_template, make_response, request, redirect, url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_

from Models.schemas.admin_schema import AdminForm
from Models.database.databasemodels import User, Role, db, Password, Carte

import datetime


def generate_available_card_number(carte_type, validity_year):
    matching_cards = Carte.query.filter(
        and_(
            Carte.carte_number.like(carte_type + '%'),
            Carte.carte_validity_year == validity_year
        )
    ).all()

    card_num_set = set([int(card.carte_number[2:]) for card in matching_cards])

    i = 1
    while True:
        if not i in card_num_set:
            return i
        i += 1


class Admin(MethodResource):
    @jwt_required()
    def post(self):
        if not (get_jwt_identity() and get_jwt_identity()['role'] == 1):
            return redirect(url_for('home', _method='GET'))

        method = request.form.get('_method')
        if method == 'CREATE':
            return self.create_carte()
        else:
            return {"message": "Invalid request"}

    @jwt_required()
    def create_carte(self):
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')

        study_year = request.form.get('study_year')
        carte_type = request.form.get('card_type')
        carte_number = request.form.get('card_number')
        carte_validity_year = request.form.get('validity_year')

        if carte_number == "":
            carte_number = generate_available_card_number(carte_type, carte_validity_year)

        carte_number = carte_type + "-" + str(carte_number)

        user = User.query.filter_by(user_email=email).first()

        message = ""

        if user is None:
            password = "password"

            try:
                new_user = User(user_first_name=firstname, user_last_name=lastname, user_email=email, user_role=2)

                db.session.add(new_user)
                db.session.flush()
                db.session.refresh(new_user)

                # Generate a salt and hash the password
                hasher = argon2.PasswordHasher()
                hashed_password = hasher.hash(password)

                newpassword = Password(user_id=new_user.user_id, password=hashed_password)

                db.session.add(newpassword)
                db.session.commit()

                message += "Account Successfully Created\n"

            except IntegrityError:
                db.session.rollback()
                return redirect(url_for('admin', _method='GET', message="This Email Already Exists"))

        user = User.query.filter_by(user_email=email).first()

        try:
            print(carte_number)
            print(carte_validity_year)
            print(study_year)
            print(user.user_id)

            new_carte = Carte(carte_number=carte_number, carte_validity_year=carte_validity_year,
                              carte_study_year=study_year, carte_user_id=user.user_id)

            db.session.add(new_carte)
            db.session.flush()
            db.session.refresh(new_carte)

            db.session.commit()

            return redirect(url_for('admin', _method='GET', message=message + "Card Successfully Created"))

        except IntegrityError:
            db.session.rollback()
            print(IntegrityError)
            return redirect(url_for('admin', _method='GET', message=message + "Error Creating card"))

    @jwt_required()
    def load_get_method(self):
        form = AdminForm()

        message = request.args.get('message')

        current_user = get_jwt_identity()

        if not current_user:
            return redirect(url_for('login', _method='GET', message=message))
        if not current_user['role'] == 1:
            return redirect(url_for('home', _method='GET', message=message))

        # form.card_number.choices = generate_available_card_number()

        users = User.query.options(joinedload(User.role)).all()
        roles = Role.query.all()

        template = render_template('admin.html', users=users, roles=roles, message=message,
                                   form=form, current_user=current_user, current_page='admin')
        response = make_response(template)
        response.headers['Content-Type'] = 'text/html'

        return response

    def get(self):
        response = make_response(redirect(url_for('login', _method='GET')))
        if not request.cookies.get('access_token_cookie'):
            return response
        try:
            response = self.load_get_method()
        except jwt.ExpiredSignatureError:
            print("Token has expired")
        return response
