from flask_apispec import MethodResource
from flask import render_template, make_response, request, session, redirect, url_for
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies, \
    jwt_required, get_jwt_identity

from Models.database.databasemodels import User, Carte
from Models.utils.limiter import limiter


class Home(MethodResource):
    decorators = [limiter.limit("10/minute")]  # Apply rate limiting to the class

    def post(self):
        return

    @jwt_required()
    def get(self):
        message = request.args.get('message')
        user = User.query.filter_by(user_email=get_jwt_identity()['email']).first()
        if not get_jwt_identity() or user is None:
            return redirect(url_for('login', _method='GET', message=message))
        if get_jwt_identity()['role'] == 1:
            return redirect(url_for('admin', _method='GET', message=message))

        carte = Carte.query.filter_by(
            carte_user_id=User.query.filter_by(user_email=get_jwt_identity()['email']).first().user_id
                                    ).first()
        domain = request.host_url
        code = carte.carte_validity_year + '_' + carte.carte_number
        link = f'{domain}scan?code={code}'

        template = render_template('home.html', message=message, link=link, user=user ,carte=carte)
        response = make_response(template)
        response.headers['Content-Type'] = 'text/html'
        return response
