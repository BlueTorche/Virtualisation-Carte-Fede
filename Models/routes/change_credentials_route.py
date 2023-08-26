from flask import render_template, make_response
from flask_apispec import MethodResource


class ChangeCredentials(MethodResource):

    def get(self):
        # TODO
        template = render_template('change_credentials.html')
        response = make_response(template)
        return response