from flask_apispec import MethodResource
from flask import jsonify, render_template, make_response, request, session, redirect, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import joinedload
import argon2

from Models.database.databasemodels import User, Password
from Models.schemas.change_credentials_schema import ChangeCredentialsForm
from Models.database.databasemodels import db


class FlutterChangePassword(MethodResource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify({"msg": "No user identity", "statusCode": 401})

        data = request.get_json()  # Récupère les données JSON de la requête

        new_password = data.get('password')
        old_password = data.get('oldPassword')

        # Query the database to check if the username and password are valid
        user = User.query.filter_by(user_email=get_jwt_identity()['email']).first()
        # Password security criteria
        if user is not None:
            if not user.check_password(old_password):
                return jsonify({"msg": "Mot de Passe Incorrect", "statusCode": 401})

            # Update user credentials if the password is valid
            if new_password:
                if not (any(c.islower() for c in new_password)
                        and any(c.isupper() for c in new_password)
                        and any(c.isdigit() for c in new_password)
                        and len(new_password) >= 8):
                    return make_response(jsonify({"msg": "Le mot de passe doit contenir au moins 8 caractères,"
                                           "une lettre en majuscule, une lettre en minuscule et un chiffre",
                                    "statusCode": 400}))

                hasher = argon2.PasswordHasher()
                hashed_password = hasher.hash(new_password)

                password_entry = Password.query.options(joinedload(Password.user)).filter_by(user=user).first()
                if password_entry:
                    password_entry.password = hashed_password

            db.session.commit()
            return jsonify({"msg": "Mot de Passe changé avec Succès", "statusCode": 200})

        return jsonify({"msg": "Erreur lors de la recherche du compte.", "statusCode": 400})
