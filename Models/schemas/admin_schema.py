
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length

from Models.utils.utils import calculate_all_validity_year, calculate_validity


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
    card_type = SelectField('Numéro de Carte', validators=[DataRequired()], choices=["F", "B"])
    card_number = IntegerField('Numéro de Carte', validators=[])
    validity_year = SelectField('Année de validité', validators=[DataRequired()],
                                choices=calculate_all_validity_year(), default=calculate_validity())
    submit = SubmitField('Créer')


