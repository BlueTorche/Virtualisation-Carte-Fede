from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, DataRequired


class GestionForm(FlaskForm):
    firstname = StringField('Prénom', validators=[])
    lastname = StringField('Nom', validators=[])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Mot de Passe', validators=[])
    copy_password = PasswordField('Confirmez  Mot de Passe', validators=[])
    submit = SubmitField('Ajouter Admin')
