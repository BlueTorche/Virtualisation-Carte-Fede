import argon2
from flask_apispec import MethodResource
from flask import jsonify, render_template, make_response, request, session, redirect, url_for
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies, \
    get_jwt_identity, jwt_required

from Models.database.databasemodels import User, Password , Role, db
from Models.schemas.gestion_schema import GestionForm

from sqlalchemy.exc import IntegrityError

class FlutterGestion(MethodResource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify({"msg": "No user identity", "statusCode": 401})
        if not current_user['role'] == 1:
            return jsonify({"msg": "Not enough right", "statusCode": 401})

        data = request.get_json()


        method = data.get('_method')
        if method == 'CREATE':
            email = data.get('email')
            firstname = data.get('firstname')
            lastname = data.get('lastname')
            password = data.get('password')

            if password:
                if not (any(c.islower() for c in password)
                        and any(c.isupper() for c in password)
                        and any(c.isdigit() for c in password)
                        and len(password) >= 8):
                    return make_response(jsonify({"msg": "Le mot de passe doit contenir au moins 8 caractères,"
                                           "une lettre en majuscule, une lettre en minuscule et un chiffre",
                                    "statusCode": 400}))

                # Query the database to check if the username and password are valid
                user = User.query.filter_by(user_email=email).first()

                if user is None:
                    try:
                        new_user = User(user_first_name=firstname, user_last_name=lastname, user_email=email, user_role=1)

                        db.session.add(new_user)
                        db.session.flush()
                        db.session.refresh(new_user)

                        # Generate a salt and hash the password
                        hasher = argon2.PasswordHasher()
                        hashed_password = hasher.hash(password)

                        newpassword = Password(user_id=new_user.user_id, password=hashed_password)

                        db.session.add(newpassword)
                        db.session.commit()

                        return make_response(jsonify({"msg": "Le compte a été créé avec succès", "statusCode": 200}))

                    except IntegrityError:
                        db.session.rollback()
                        return make_response(jsonify({"msg": "L'utilisateur existe déjà", "statusCode": 400}))

                return make_response(jsonify({"msg": "L'utilisateur existe déjà", "statusCode": 400}))
            return make_response(jsonify({"msg": "Pas de mot de passe donné", "statusCode": 400}))

        elif method == 'DELETE':
            email = data.get('email')

            if email == current_user['email']:
                return make_response(jsonify({"msg": "Vous ne pouvez pas supprimer votre compte", "statusCode": 400}))

            user = User.query.filter_by(user_email=email).first()

            if not user:
                return make_response(jsonify({"msg": "Administrateur non trouvé", "statusCode": 400}))

            db.session.delete(user)
            db.session.commit()

            return make_response(jsonify({"msg": "Administrateur supprimé avec succès", "statusCode": 200}))

        return make_response(jsonify({"msg": f"Invalide request {method}", "statusCode": 404}))

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify({"msg": "No user identity", "statusCode": 401})
        if not current_user['role'] == 1:
            return jsonify({"msg": "Not enough right", "statusCode": 401})

        users = User.query.filter_by(user_role=1).all()

        response = [["Email", "Prénom", "Nom", "Action"]]
        for user in users:
            response.append([user.user_email, user.user_first_name, user.user_last_name])

        return make_response(jsonify({"msg": response, "statusCode": 200}))

