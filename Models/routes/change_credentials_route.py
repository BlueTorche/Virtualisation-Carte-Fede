from flask_apispec import MethodResource
from flask import render_template, make_response, request, session, redirect, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm import joinedload
import argon2

from Models.database.databasemodels import User, Password
from Models.schemas.change_credentials_schema import ChangeCredentialsForm
from Models.database.databasemodels import db


class ChangeCredentials(MethodResource):

    @jwt_required()
    def post(self):
        if not (get_jwt_identity()):
            redirect(url_for('login', _method='GET'))

        new_firstname = request.form.get('firstname')
        new_lastname = request.form.get('lastname')
        new_email = request.form.get('email')
        new_password = request.form.get('new_password')
        copy_new_password = request.form.get('copy_new_password')
        old_password = request.form.get('old_password')

        if not new_password == copy_new_password:
            return redirect(url_for('changecredentials', _method='GET',
                                    message='The new passwords are different and should be the same.'))


        # Query the database to check if the username and password are valid
        user = User.query.filter_by(user_email=get_jwt_identity()['email']).first()
        # Password security criteria

        if user is not None:
            if not user.check_password(old_password):
                return redirect(url_for('changecredentials', _method='GET',
                                        message='Your credentials have not been updated. Your password is incorrect.'))
            # Update user credentials if the password is valid
            if new_password:
                if not (any(c.islower() for c in new_password)
                        and any(c.isupper() for c in new_password)
                        and any(c.isdigit() for c in new_password)
                        and len(new_password) >= 8):
                    return redirect(
                        url_for('register', _method='GET', message='Votre mot de passe doit au moins faire 8 caractère,'
                                                                   ' contenir une lettre en majuscule, une lettre en'
                                                                   ' minuscule et un chiffre.'))

                hasher = argon2.PasswordHasher()
                hashed_password = hasher.hash(new_password)

                password_entry = Password.query.options(joinedload(Password.user)).filter_by(user=user).first()
                if password_entry:
                    password_entry.password = hashed_password

            if new_firstname:
                user.user_first_name = new_firstname
            if new_lastname:
                user.user_last_name = new_lastname
            if new_email:
                user.user_email = new_email

            db.session.commit()
            return redirect(url_for('home', _method='GET', message='Your credentials have been successfully updated.'))

        return redirect(url_for('changecredentials', _method='GET', message='Error finding your user account.'))

    @jwt_required()
    def get(self):
        if not (get_jwt_identity()):
            redirect(url_for('login', _method='GET'))

        current_user = get_jwt_identity();

        form = ChangeCredentialsForm()
        message = request.args.get('message')
        template = render_template('change_credentials.html', form=form, message=message,
                                   current_user=current_user, current_page='changecredentials')
        response = make_response(template)
        response.headers['Content-Type'] = 'text/html'
        return response
