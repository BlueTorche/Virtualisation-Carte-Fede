import argon2
from flask_apispec import MethodResource
from flask import render_template, make_response, request, session, redirect, url_for
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies, \
    get_jwt_identity, jwt_required

from Models.database.databasemodels import User, Password, Role
from Models.schemas.login_schema import LoginForm
from Models.utils.limiter import limiter


class Login(MethodResource):
    decorators = [limiter.limit("10/minute")]  # Apply rate limiting to the class

    def post(self):
        # Handle login logic here
        email = request.form.get('email')
        password = request.form.get('password')

        # Query the database to check if the username and password are valid
        user = User.query.filter_by(user_email=email).first()

        if user is not None and user.check_password(password):
            # User authentication successful
            identity = {'email': email, 'role': user.user_role}
            access_token = create_access_token(identity=identity)
            refresh_token = create_refresh_token(identity=identity)

            response = redirect(url_for('home', _method='GET'))
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response
        return redirect(url_for('login', _method='GET', message="Invalid Email or Password"))

    def get(self):
        message = request.args.get('message')

        if request.cookies.get('access_token_cookie'):
            return make_response(redirect(url_for('home', _method='GET', message=message)))

        form = LoginForm()
        template = render_template('login.html', form=form, message=message)
        response = make_response(template)
        response.headers['Content-Type'] = 'text/html'
        return response

