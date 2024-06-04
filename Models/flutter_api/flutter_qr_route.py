import argon2
from flask_apispec import MethodResource
from flask import jsonify, render_template, make_response, request, session, redirect, url_for
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies, \
    get_jwt_identity, jwt_required

from Models.database.databasemodels import Carte, User, db
from Models.schemas.gestion_schema import GestionForm

from sqlalchemy.exc import IntegrityError


class FlutterQRCode(MethodResource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify({"msg": "No user identity", "statusCode": 401})

        user = User.query.filter_by(user_email=current_user['email']).first()

        if not user:
            return jsonify({"msg": "No card for user", "statusCode": 200})

        carte = Carte.query.filter_by(
            carte_user_id=user.user_id
        ).first()
        domain = request.host_url
        code = carte.carte_validity_year + '_' + carte.carte_number
        link = f'{domain}scan?code={code}'

        response = {"link": link, "card_number": carte.carte_number,
                    "card_year": carte.carte_validity_year, "card_study": carte.carte_study_year,
                    "user_name": user.user_last_name, "user_first_name": user.user_first_name}

        return make_response(jsonify({"msg": response, "statusCode": 200}))
