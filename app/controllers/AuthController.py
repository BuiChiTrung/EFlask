from flask import Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

from app.util  import json_response
from app.models.User import User
from app.repositories.UserRepository import UserRepository

repository = UserRepository('app.models.User', 'User')
auth_blueprint = Blueprint('auth_blueprint', __name__)

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField()

class SignUpForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min = 10, message='Username minium length is %(min)d.')])
    password = PasswordField(validators=[DataRequired(), Length(min = 6, message='Username minium length is %(min)d.')])
    password_confirmation = PasswordField(validators=[DataRequired(), EqualTo('password', message='Password and confirmation password does not match.')])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

@auth_blueprint.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form, meta={'csrf': False})

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return json_response(True, 'Login successfully.')

    return json_response(False, 'Invalid username or password.', 400)

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    form = SignUpForm(request.form, meta={'csrf': False})

    if form.validate_on_submit():
        repository.store({'username': form.username.data, 'password': form.password.data})   
        return json_response(True, 'Your account has been registered.')
        
    return json_response(False, form.errors, 400)

@auth_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return json_response(True, 'Logged out')
    
