import json
import os
import re
import requests
import random
import string

from dotenv import load_dotenv
from flask import Blueprint, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from twilio.rest import Client
from werkzeug.security import generate_password_hash
from wtforms import StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

from app.util  import json_response, get_error_list
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
    password = PasswordField(validators=[DataRequired(), Length(min = 6, message='Password minium length is %(min)d.')])
    phone_number = StringField(validators=[DataRequired()])
    password_confirmation = PasswordField(validators=[DataRequired(), EqualTo('password', message='Password and confirmation password does not match.')])

    def validate_username(self, field):
        if repository.find({'username': field.data}) != []:
            raise ValidationError('Username already in use.')
        
    def validate_phone_number(self, field):
        if re.search('^[0-9]{9,11}$', field.data) == None:
            raise ValidationError('Invalid phone number.')
        elif repository.find({'phone_number': reformat_phone_number(field.data)}) != []:
            raise ValidationError('Phone number already in use.')
        

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(validators=[DataRequired()])
    new_password = PasswordField(validators=[DataRequired(), Length(min = 6, message='Password minium length is %(min)d.')])
    password_confirmation = PasswordField(validators=[DataRequired(), EqualTo('new_password', message='New password and confirmation password does not match.')])

@auth_blueprint.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form, meta={'csrf': False})

    if form.validate_on_submit():
        user = repository.find({'username': form.username.data})#User.query.filter_by(username=form.username.data).first()
        if len(user) > 0 and user[0].verify_password(form.password.data):
            user = user[0]
            login_user(user, form.remember_me.data)
            return json_response(True, user.as_dict())

    return json_response(False, 'Invalid username or password.', 400)

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    form = SignUpForm(request.form, meta={'csrf': False})

    if form.validate_on_submit():
        repository.store({
            'username': form.username.data, 
            'password': form.password.data,
            'phone_number': reformat_phone_number(form.phone_number.data)
        })   
        return json_response(True, 'Your account has been created.', 201)
        
    return json_response(False, get_error_list(form.errors), 400)

@auth_blueprint.route('/change-password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form, meta={'csrf': False})
    
    if form.validate_on_submit():
        if current_user.verify_password(form.current_password.data):
            repository.update(current_user.id, {'password_hash': generate_password_hash(form.new_password.data)})
            return json_response(True, 'Successfully updated password.')
        return json_response(False, 'Current password is not correct.', 400)  
    return json_response(False, get_error_list(form.errors), 400)
        
@auth_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return json_response(True, 'Logged out')
    
@auth_blueprint.route('/google-login', methods=['POST'])
def google_login():
    url = "https://www.googleapis.com/oauth2/v1/userinfo"
    access_token = request.form['access_token']
    headers = {
        'Authorization': f'Bearer  {access_token}'
    }
    response = requests.request("GET", url, headers=headers, data={})
    response = json.loads(response.text)
    # return response

    if 'error' in response:
        return json_response(False, 'Invalid access token', 401)
    
    email = response['email']
    user = repository.find({'email': email})
    if len(user) == 0:
        user = repository.store({'email': email, 'username': response['name']})
    else:
        user = user[0]
    
    login_user(user, True) 
    return json_response(True, user.as_dict())

@auth_blueprint.route('/forgot-password', methods=['POST'])
def forgot_password():
    phone_number = reformat_phone_number(request.form['phone_number'])
    users = repository.find({'phone_number': phone_number})
    
    if users == []:
        return json_response(False, 'No account matches phone number', 400)
    else:
        user = users[0]
        new_password = random_string_generator()
        repository.update(user.id, {'password_hash': generate_password_hash(new_password)})
        try: 
            sent_new_pass_via_sms(new_password, user.phone_number)
        except Exception:
            return json_response(False, 'Invalid phone number', 400)
        
        return json_response(True, 'New password is sent to your phone number')

def reformat_phone_number(phone_number):
    return f'+84{phone_number}'

def random_string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def sent_new_pass_via_sms(new_password, receiver):
    load_dotenv()
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=f'EFlask new password: {new_password}',
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        to=receiver
    )