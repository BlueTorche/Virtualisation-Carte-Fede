from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=50)])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Log In')
