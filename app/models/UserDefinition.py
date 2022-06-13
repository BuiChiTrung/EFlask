from app import db
from app.models.Base import Base

class UserDefinition(db.Model, Base):
    __tablename__ = 'user_definitions'

    id = db.Column(db.Integer, primary_key=True)
    meaning = db.Column(db.String(1000), nullable=False)
    lexical_category = db.Column(db.String(15))
    example = db.Column(db.String(1000))

    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False)

    cards = db.relationship('Card', backref='user_def', lazy='dynamic', cascade='all, delete-orphan')
