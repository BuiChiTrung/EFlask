import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Trung123@127.0.0.1/EFlask"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'very secret key'    

    db.init_app(app)
    login_manager.init_app(app)
    
    from app.controllers import word_blueprint, auth_blueprint, deck_blueprint, card_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(word_blueprint, url_prefix='/words')
    app.register_blueprint(deck_blueprint, url_prefix='/decks')
    app.register_blueprint(card_blueprint, url_prefix='/cards')

    return app