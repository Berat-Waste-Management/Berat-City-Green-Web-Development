from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, SelectMultipleField
from wtforms.validators import  ValidationError, DataRequired, Length, Email, Optional

from app import db
import sqlalchemy as sqla

from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

class BookingForm(FlaskForm):
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=1, max=250)])
    machine_type = SelectMultipleField('Machine Selection',
    choices=[
        ('washer', 'Washer'),
        ('dryer', 'Dryer'),
    ],
    option_widget=CheckboxInput(),
    widget=ListWidget(prefix_label=False))

    
    submit = SubmitField('Post')


class ReportForm(FlaskForm):   
    reason = TextAreaField('Issue Description', validators=[DataRequired(), Length(min=10, max=500)])

    submit = SubmitField('Submit Report')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[('1', '1 Star'), ('2', '2 Stars'), ('3', '3 Stars'), ('4', '4 Stars'), ('5', '5 Stars')], validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[Length(max=500)])
    submit = SubmitField('Submit Review')


