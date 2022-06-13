from app import db
from app.models.Base import Base
from app.models.SystemDefinition import SystemDefinition

class Word(db.Model, Base):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), nullable=False, unique=True)
    ipa = db.Column(db.String(50))
    audio_url = db.Column(db.String(120))
    img_url = db.Column(db.String(300)) 
    vi_meaning = db.Column(db.String(20))

    sys_defs = db.relationship('SystemDefinition', backref='word', lazy='dynamic', cascade='all, delete-orphan')
