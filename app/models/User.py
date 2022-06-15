from email.policy import default
from enum import unique
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login_manager
from app.models.Base import Base

class User(UserMixin, db.Model, Base):
    __tablename__ = 'users'
    exclude_fields = ['password_hash']
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True, nullable=False)
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    avatar_url = db.Column(db.String(100), default='default.png')
    phone_number = db.Column(db.String(15), unique=True)
    
    decks = db.relationship('Deck', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def write_user_id_to_session(user_id):
        return User.query.get(user_id)
