import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Trung123@127.0.0.1/EFlask"
    # 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
    db.init_app(app)
    
    return app