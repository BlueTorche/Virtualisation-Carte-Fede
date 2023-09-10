from flask_wtf import FlaskForm
from wtforms import SubmitField

class ViewForm(FlaskForm):
    submit = SubmitField('')
