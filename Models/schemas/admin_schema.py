from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Email, Length

from Models.database.databasemodels import Carte


def calculate_validity():
    today = datetime.now()

    if today.month >= 9:  # If current month is September or later
        start_year = today.year
    else:
        start_year = today.year - 1

    end_year = start_year + 1
    return f"{start_year}-{end_year}"

def calculate_all_validity_year():
    this_year = calculate_validity()
    year1 = int(this_year.split("-")[0])

    all_validity = []

    for i in range(-5,6):
        all_validity.append(str(year1+i)+"-"+str(year1+i+1))

    return all_validity

class AdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=50)])
    lastname = StringField('Nom', validators=[DataRequired(), Length(min=2, max=50)])
    firstname = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=50)])
    study_year = SelectField('Année et Option', validators=[DataRequired()], choices=[
        ('BAB1', 'BAB1'),
        ('BAB1 Archi', 'BAB1 Archi'),
        ('BAB2', 'BAB2'),
        ('BAB2 Archi', 'BAB2 Archi'),
        ('BAB3 Archi', 'BAB3 Archi'),
        ('BAB3 Chimie', 'BAB3 Chimie'),
        ('BAB3 Elec', 'BAB3 Elec'),
        ('BAB3 IG', 'BAB3 IG'),
        ('BAB3 Meca', 'BAB3 Meca'),
        ('BAB3 Mines', 'BAB3 Mines'),
        ('MAB1 Archi', 'MAB1 Archi'),
        ('MAB1 Chimie', 'MAB1 Chimie'),
        ('MAB1 Elec', 'MAB1 Elec'),
        ('MAB1 IG', 'MAB1 IG'),
        ('MAB1 Meca', 'MAB1 Meca'),
        ('MAB1 Mines', 'MAB1 Mines'),
        ('MAB2 Archi', 'MAB2 Archi'),
        ('MAB2 Chimie', 'MAB2 Chimie'),
        ('MAB2 Elec', 'MAB2 Elec'),
        ('MAB2 IG', 'MAB2 IG'),
        ('MAB2 Meca', 'MAB2 Meca'),
        ('MAB2 Mines', 'MAB2 Mines'),
        ('Exté', 'Exté'),
        ('Autre', 'Autre'),
    ])
    card_number = SelectField('Numéro de Carte', validators=[DataRequired()],
                              choices=[])
    validity_year = SelectField('Année de validité', validators=[DataRequired()],
                                choices=calculate_all_validity_year(), default=calculate_validity())
    submit = SubmitField('Créer')


