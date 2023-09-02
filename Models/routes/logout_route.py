from flask_apispec import MethodResource
from flask import redirect, url_for
from flask_jwt_extended import unset_jwt_cookies


class Logout(MethodResource):

    def get(self):
        response = redirect(url_for('login', _method='GET'))
        unset_jwt_cookies(response)
        return response
