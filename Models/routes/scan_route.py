from flask import render_template, make_response, request
from flask_apispec import MethodResource

from Models.database.databasemodels import Carte, User
from utils import calculate_validity


class Scan(MethodResource):

    def get(self):
        code = request.args.get('code').split('_')  # Get the value of the 'info' parameter

        carte, user = None, None
        if len(code) == 2:
            validity_year, number = code[0], code[1]

            carte = Carte.query.filter_by(
                carte_validity_year=validity_year,
                carte_number=number
            ).first()
        elif len(code) == 1:
            number = code[0]

            carte = Carte.query.filter_by(
                carte_validity_year=calculate_validity(),
                carte_number=number
            ).first()

        if carte is not None:
            user = User.query.filter_by(
                user_id=carte.carte_user_id
            ).first()

        template = render_template('scan.html', carte=carte, user=user)
        response = make_response(template)
        return response
