from enum import unique
from sqlalchemy import Integer, PrimaryKeyConstraint, null

from app import db
from app.models.SystemDefinition import SystemDefinition

class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), nullable=False, unique=True)
    ipa = db.Column(db.String(50))
    audio_url = db.Column(db.String(120))
    img_url = db.Column(db.String(300)) 

    sys_defs = db.relationship('SystemDefinition', backref='word', lazy='dynamic')

    def __repr__(self):
        return (f'<"word": "{self.word}",'
                f'"ipa": "{self.ipa}",'
                f'"img_url": "{self.img_url}"'
                '>')