import json
import random
import string

from flask import Blueprint, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash

from app.repositories.UserRepository import UserRepository
from app.util.forms import LoginForm, SignUpForm, ChangePasswordForm
from app.util.others import json_response, get_error_list
from app.util.services import google_oauth, twilio_sent_new_pass_via_sms

repository = UserRepository('app.models.User', 'User')
auth_blueprint = Blueprint('auth_blueprint', __name__)

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
            'phone_number': form.phone_number.data
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
    response = json.loads(google_oauth(request.form['access_token']).text)

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
    users = repository.find({'phone_number': request.form['phone_number']})
    
    if users == []:
        return json_response(False, 'No account matches phone number', 400)
    else:
        user = users[0]
        new_password = random_string_generator()
        repository.update(user.id, {'password_hash': generate_password_hash(new_password)})
        try: 
            twilio_sent_new_pass_via_sms(new_password, f'+84{user.phone_number}')
        except Exception:
            return json_response(False, 'Invalid phone number', 400)
        
        return json_response(True, 'New password is sent to your phone number')


def random_string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))