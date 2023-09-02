from flask import render_template, make_response
from flask_apispec import MethodResource
from flask_jwt_extended import get_jwt_identity, jwt_required


class ChangeCredentials(MethodResource):

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        # TODO
        template = render_template('change_credentials.html', current_user=current_user)
        response = make_response(template)
        return response