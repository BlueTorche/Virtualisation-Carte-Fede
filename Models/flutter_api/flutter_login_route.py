from flask_apispec import MethodResource
from flask import jsonify, render_template, make_response, request, session, redirect, url_for
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies
from flask_wtf.csrf import generate_csrf

from Models.database.databasemodels import User, Password , Role
from Models.schemas.login_schema import LoginForm
from Models.utils.limiter import limiter

class FlutterLogin(MethodResource):
    def post(self):
        data = request.get_json()  # Récupère les données JSON de la requête
        email = data.get('email')  # Récupère l'email
        password = data.get('password')  # Récupère le mot de passe
        user = User.query.filter_by(user_email=email).first()

        if user is not None and user.check_password(password):
            identity = {'email': email, 'role': user.user_role}
            access_token = create_access_token(identity=identity)
            refresh_token = create_refresh_token(identity=identity)

            response_body = jsonify({"msg": "Successful Connexion",
                                     "role": user.role.role_id,
                                     "statusCode": 200})
            response = make_response(response_body)
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)

            return response
        return jsonify({"msg": "Connexion Refused", "statusCode": 401})


