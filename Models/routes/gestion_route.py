import argon2
from flask_apispec import MethodResource
from flask import render_template, make_response, request, session, redirect, url_for
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies, \
    get_jwt_identity, jwt_required

from Models.database.databasemodels import User, Password , Role, db
from Models.schemas.gestion_schema import GestionForm

from sqlalchemy.exc import IntegrityError

class Gestion(MethodResource):
    @jwt_required()
    def post(self):
        method = request.form.get('_method')
        if method == 'CREATE':
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = request.form.get('email')
            password = request.form.get('password')
            copy_password = request.form.get('copy_password')

            if not password == copy_password:
                return redirect(url_for('gestion', _method='GET',
                                        message='The new passwords are different and should be the same.'))
            if password:
                if not (any(c.islower() for c in password)
                        and any(c.isupper() for c in password)
                        and any(c.isdigit() for c in password)
                        and len(password) >= 8):
                    return redirect(
                        url_for('gestion', _method='GET', message='Votre mot de passe doit au moins faire 8 caractères,'
                                                                   ' contenir une lettre en majuscule, une lettre en'
                                                                   ' minuscule et un chiffre.'))
                # Query the database to check if the username and password are valid
                user = User.query.filter_by(user_email=email).first()

                if user is None:
                    try:
                        new_user = User(user_first_name=firstname, user_last_name=lastname, user_email=email, user_role=1)

                        db.session.add(new_user)
                        db.session.flush()
                        db.session.refresh(new_user)

                        # Generate a salt and hash the password
                        hasher = argon2.PasswordHasher()
                        hashed_password = hasher.hash(password)

                        newpassword = Password(user_id=new_user.user_id, password=hashed_password)

                        db.session.add(newpassword)
                        db.session.commit()

                        return redirect(url_for('gestion', _method='GET', message="Account Successfully Created"))
                    except IntegrityError:
                        db.session.rollback()
                        return redirect(url_for('gestion', _method='GET', message="This Email Already Exists"))

                return redirect(url_for('gestion', _method='GET', message="That User already exist"))
            return redirect(url_for('gestion', _method='GET', message="Password is null"))
        if method == 'DELETE':
            user_id = request.form.get('user_id')

            user = User.query.filter_by(user_id=user_id).first()

            if user.user_email == get_jwt_identity()['email']:
                return redirect(url_for('gestion', _method='GET', message="You cannot delete your own account."))

            if not user:
                return {"message": "Card not found"}

            db.session.delete(user)
            db.session.commit()

            return redirect(url_for('gestion', _method='GET', message="Account Delete successfully"))
        return {"message": "Invalid request"}


    @jwt_required()
    def load_get_method(self):
        message = request.args.get('message')

        current_user = get_jwt_identity()

        if not current_user:
            return redirect(url_for('login', _method='GET', message=message))
        if not current_user['role'] == 1:
            return redirect(url_for('home', _method='GET', message=message))

        users = User.query.filter_by(user_role=1).all()

        current_user = get_jwt_identity()

        form = GestionForm()
        template = render_template('gestion.html', form=form, message=message, users=users,
                                   current_user=current_user, current_page='gestion')
        response = make_response(template)
        response.headers['Content-Type'] = 'text/html'
        return response

    def get(self):
        if not request.cookies.get('access_token_cookie'):
            return make_response(redirect(url_for('login', _method='GET')))
        return self.load_get_method()

