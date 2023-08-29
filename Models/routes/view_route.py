from flask import render_template, make_response, request, redirect, url_for
from flask_apispec import MethodResource
from flask_jwt_extended import jwt_required, get_jwt_identity

from Models.database.databasemodels import Carte, User


class View(MethodResource):

    @jwt_required()
    def get(self):
        message = request.args.get('message')

        if not get_jwt_identity():
            return redirect(url_for('login', _method='GET', message=message))
        if not get_jwt_identity()['role'] == 1:
            return redirect(url_for('home', _method='GET', message=message))

        cartes = Carte.query.all()

        infos = []

        for carte in cartes:
            user = User.query.filter_by(
                user_id=carte.carte_user_id
            ).first()

            if user is not None:
                infos.append({"validity_year": carte.carte_validity_year,
                              "number": carte.carte_number,
                              "first_name": user.user_first_name,
                              "last_name": user.user_last_name,
                              })

        template = render_template('view.html', infos=infos)
        response = make_response(template)
        return response
