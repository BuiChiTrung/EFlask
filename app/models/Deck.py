from app import db
from app.models.Base import Base

class Deck(db.Model, Base):
    __tablename__ = 'decks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    cards = db.relationship('Card', backref='deck', lazy='dynamic', cascade='all, delete-orphan') 