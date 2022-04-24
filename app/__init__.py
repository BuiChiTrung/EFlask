import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Trung123@127.0.0.1/EFlask"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
    db.init_app(app)
    
    from app.controllers.WordController import word_blueprint
    app.register_blueprint(word_blueprint)

    return app