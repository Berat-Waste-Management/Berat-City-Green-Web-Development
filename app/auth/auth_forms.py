from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Email, Length
from app.main.models import User
from wtforms.widgets import ListWidget, Select

from app import db
import sqlalchemy as sqla


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(), Email()])

    address = TextAreaField('Address', [Length(min=0, max=200)])

    password = PasswordField('Password', validators=[DataRequired()])

    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    user_type = SelectField('Account Type',
    choices=[
        # ('User', 'User'),
        ('Driver', 'Driver')
    ],
    validators=[DataRequired()] )

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Sign In')


class AdminRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    location = SelectField('Laundromat Location', 
    choices=[
        ('1', 'West'),
        ('2', 'Fruit'),
        ('3', 'Oak'),
        ('4', 'CedarA'),
        ('5', 'CedarB'),
        ('6', 'CedarC')
    ], validators=[DataRequired()] 
    )

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class SSOSetupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    user_type = SelectField('Account Type',
        choices=[('User', 'User'), ('Driver', 'Driver'), ('Admin', 'Admin')],
        validators=[DataRequired()]
    )
    location = SelectField('Location (Admins only)',
        choices=[
            ('', 'N/A'),
            ('1', 'West'), ('2', 'Fruit'), ('3', 'Oak'),
            ('4', 'CedarA'), ('5', 'CedarB'), ('6', 'CedarC')
        ],
        validators=[]
    )
    submit = SubmitField('Complete Registration')

    def validate_location(self, location):
        if self.user_type.data == 'Admin' and not location.data:
            raise ValidationError('Admins must select a location.')