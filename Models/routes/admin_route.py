import argon2
from flask_apispec import MethodResource
from flask import render_template, make_response, request, redirect, url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from flask_jwt_extended import jwt_required, get_jwt_identity

from Models.schemas.admin_schema import AdminForm
from Models.database.databasemodels import User, Role, db, Password, Carte

import datetime


def generate_available_card_number():
    all_cartes = Carte.query.all()
    card_num_set = set([int(card.carte_number[2:]) for card in all_cartes])

    max_size = 1000
    max_select_box_size = 20

    to_return = []
    for num in range(1, max_size+1):
        if num not in card_num_set:
            to_return.append(num)
            if len(to_return) >= max_select_box_size:
                break

    return to_return


class Admin(MethodResource):
    @jwt_required()
    def post(self):
        if not (get_jwt_identity() and get_jwt_identity()['role'] == 3):
            redirect(url_for('home', _method='GET'))

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

        carte_number = request.form.get('card_number')
        carte_validity_year = request.form.get('validity_year')

        user = User.query.filter_by(user_email=email).first()

        message = ""

        # if not (any(c.islower() for c in password)
        #         and any(c.isupper() for c in password)
        #         and any(c.isdigit() for c in password)
        #         and any(c in '@$!%*?&' for c in password)):
        #     return redirect(url_for('register', _method='GET', message='Password should contain at least one uppercase '
        #                                                                'letter, one lowercase letter, one digit, '
        #                                                                'and one special character.'))

        if user is None:
            password = "password"

            try:
                newuser = User(user_first_name=firstname, user_last_name=lastname, user_email=email, user_role=2)

                db.session.add(newuser)
                db.session.flush()
                db.session.refresh(newuser)

                # Generate a salt and hash the password
                hasher = argon2.PasswordHasher()
                hashed_password = hasher.hash(password)

                newpassword = Password(user_id=newuser.user_id, password=hashed_password)

                db.session.add(newpassword)
                db.session.commit()

                message += "Account Successfully Created\n"

            except IntegrityError:
                db.session.rollback()
                return redirect(url_for('admin', _method='GET', message="This Email Already Exists"))

        user = User.query.filter_by(user_email=email).first()

        try:

            newcarte = Carte(carte_number=carte_number, carte_validity_year=carte_validity_year,
                             carte_study_year=study_year, carte_user_id=user.user_id)

            db.session.add(newcarte)
            db.session.flush()
            db.session.refresh(newcarte)

            db.session.commit()

            return redirect(url_for('login', _method='GET', message=message + "Card Successfully Created"))

        except IntegrityError:
            db.session.rollback()
            print(IntegrityError)
            return redirect(url_for('admin', _method='GET', message=message + "Error Creating card"))

    @jwt_required()
    def get(self):
        form = AdminForm()

        form.card_number.choices = generate_available_card_number()

        message = request.args.get('message')

        if not get_jwt_identity():
            return redirect(url_for('login', _method='GET', message=message))
        if not get_jwt_identity()['role'] == 1:
            return redirect(url_for('home', _method='GET', message=message))

        users = User.query.options(joinedload(User.role)).all()
        roles = Role.query.all()

        template = render_template('admin.html', users=users, roles=roles, message=message, form=form)
        response = make_response(template)
        response.headers['Content-Type'] = 'text/html'
        return response
