from flask import Blueprint, request, jsonify
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

from app.models.User import User
from app import db

auth_blueprint = Blueprint('auth_blueprint', __name__)

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField()

@auth_blueprint.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form, meta={'csrf': False})

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return jsonify({
                'success': True,
                'message': 'Login successfully.'
            })

    return jsonify({
        'success': False,
        'message': 'Invalid username or password.'
    }), 400


class SignUpForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min = 10, message='Username minium length is %(min)d.')])
    password = PasswordField(validators=[DataRequired(), Length(min = 6, message='Username minium length is %(min)d.')])
    password_confirmation = PasswordField(validators=[DataRequired(), EqualTo('password', message='Password and confirmation password does not match.')])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    print('asf;lkahdfaksdjf;ashdfl;shdfhkjsd')
    form = SignUpForm(request.form, meta={'csrf': False})

    if form.validate_on_submit():   
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Your account has been registered successfully.'
        })

    return jsonify({
        'success': False,
        'message': form.errors
    }), 400
