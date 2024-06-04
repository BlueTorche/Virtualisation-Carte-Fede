import argon2
from flask_apispec import MethodResource
from flask import jsonify, render_template, make_response, request, session, redirect, url_for
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies, \
    get_jwt_identity, jwt_required

from Models.database.databasemodels import Carte, User, db
from Models.schemas.gestion_schema import GestionForm

from sqlalchemy.exc import IntegrityError

class FlutterView(MethodResource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify({"msg": "No user identity", "statusCode": 401})
        if not current_user['role'] == 1:
            return jsonify({"msg": "Not enough right", "statusCode": 401})

        data = request.get_json()  # Récupère les données JSON de la requête


        method = data.get('_method')
        if method == 'DELETE':
            card = data.get('card')

            card = Carte.query.filter_by(carte_id=card).first()

            if not card:
                return make_response(jsonify({"msg": "Carte non trouvé", "statusCode": 400}))

            db.session.delete(card)
            db.session.commit()

            return make_response(jsonify({"msg": "Carte supprimé avec succès", "statusCode": 200}))

        return make_response(jsonify({"msg": f"Invalide request {method}", "statusCode": 404}))

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify({"msg": "No user identity", "statusCode": 401})
        if not current_user['role'] == 1:
            return jsonify({"msg": "Not enough right", "statusCode": 401})

        cartes = Carte.query.all()

        response = [["Annee de Validité", "Numéro", "Prénom", "Nom", "Année d'étude", "Action"]]

        for carte in cartes:
            user = User.query.filter_by(
                user_id=carte.carte_user_id
            ).first()

            if user is not None:
                response.append([carte.carte_validity_year,
                                 carte.carte_number,
                                 user.user_first_name,
                                 user.user_last_name,
                                 carte.carte_study_year,
                                 carte.carte_id,
                              ])

        return make_response(jsonify({"msg": response, "statusCode": 200}))

