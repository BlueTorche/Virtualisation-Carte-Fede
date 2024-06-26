from flask_apispec import MethodResource
from flask import render_template, make_response, request, session, redirect, url_for
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies, \
    jwt_required, get_jwt_identity

from Models.database.databasemodels import User, Carte
from Models.utils.limiter import limiter

from jwt import ExpiredSignatureError


class Home(MethodResource):
    decorators = [limiter.limit("10/minute")]  # Apply rate limiting to the class

    def post(self):
        return

    @jwt_required()
    def load_get_method(self):
        message = request.args.get('message')
        user = User.query.filter_by(user_email=get_jwt_identity()['email']).first()

        current_user = get_jwt_identity()

        if not current_user or user is None:
            return redirect(url_for('login', _method='GET', message=message))
        if current_user['role'] == 1:
            return redirect(url_for('admin', _method='GET', message=message))

        carte = Carte.query.filter_by(
            carte_user_id=User.query.filter_by(user_email=current_user['email']).first().user_id
        ).first()
        domain = request.host_url
        code = carte.carte_validity_year + '_' + carte.carte_number
        link = f'{domain}scan?code={code}'

        template = render_template('home.html', message=message, link=link, user=user,
                                   carte=carte, current_user=current_user, current_page='home')
        response = make_response(template)
        response.headers['Content-Type'] = 'text/html'
        return response

    def get(self):
        response = make_response(redirect(url_for('logout', _method='GET')))
        if not request.cookies.get('access_token_cookie'):
            return response
        try:
            response = self.load_get_method()
        except ExpiredSignatureError:
            print("Token has expired")
        return response
