import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

from app.repositories.UserRepository import UserRepository

user_repository = UserRepository('app.models.User', 'User')

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField()


class SignUpForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min = 10, message='Username minium length is %(min)d.')])
    password = PasswordField(validators=[DataRequired(), Length(min = 6, message='Password minium length is %(min)d.')])
    phone_number = StringField(validators=[DataRequired()])
    password_confirmation = PasswordField(validators=[DataRequired(), EqualTo('password', message='Password and confirmation password does not match.')])

    def validate_username(self, field):
        if user_repository.find({'username': field.data}) != []:
            raise ValidationError('Username already in use.')
        
    def validate_phone_number(self, field):
        if re.search('^[0-9]{9,11}$', field.data) == None:
            raise ValidationError('Invalid phone number.')
        elif user_repository.find({'phone_number': field.data}) != []:
            raise ValidationError('Phone number already in use.')
        
        
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(validators=[DataRequired()])
    new_password = PasswordField(validators=[DataRequired(), Length(min = 6, message='Password minium length is %(min)d.')])
    password_confirmation = PasswordField(validators=[DataRequired(), EqualTo('new_password', message='New password and confirmation password does not match.')])