from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email


class ChangeCredentialsForm(FlaskForm):
    firstname = StringField('Nouveau Prénom', validators=[])
    lastname = StringField('Nouveau Nom', validators=[])
    email = StringField('Nouvel Email', validators=[Email()])
    new_password = PasswordField('Nouveau Mot de Passe', validators=[])
    copy_new_password = PasswordField('Validez Nouveau Mot de Passe', validators=[])
    old_password = PasswordField('Ancien Mot de Passe', validators=[InputRequired()])
    submit = SubmitField('Change Credentials')
