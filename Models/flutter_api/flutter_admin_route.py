import argon2
from flask_apispec import MethodResource
from flask import jsonify, render_template, make_response, request, redirect, url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_

from Models.utils.utils import generate_available_card_number
from Models.schemas.admin_schema import AdminForm
from Models.database.databasemodels import User, Role, db, Password, Carte

import datetime


class FlutterAdmin(MethodResource):

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify({"msg": "No user identity", "statusCode": 401})
        if not current_user['role'] == 1:
            return jsonify({"msg": "Not enough right", "statusCode": 401})

        data = request.get_json()

        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')

        study_year = data.get('study_year')
        carte_type = "F"
        carte_number = data.get('card_number')
        carte_validity_year = data.get('validity_year')

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
                return jsonify({"msg": "This Email Already Exists", "statusCode": 400})

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

            return jsonify({"msg": message + "Card Successfully Created", "statusCode": 200})

        except IntegrityError:
            db.session.rollback()
            print(IntegrityError)
            return jsonify({"msg": message + "Error Creating card", "statusCode": 400})