from dotenv import load_dotenv
import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOSTNAME')}:{os.getenv('PORT')}/{os.getenv('DATABASE')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  
    print(app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)
    login_manager.init_app(app)
    
    from app.controllers import word_blueprint, auth_blueprint, deck_blueprint, card_blueprint, user_blueprint, video_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(word_blueprint, url_prefix='/words')
    app.register_blueprint(deck_blueprint, url_prefix='/decks')
    app.register_blueprint(card_blueprint, url_prefix='/cards')
    app.register_blueprint(video_blueprint, url_prefix='/videos')
    
    return app