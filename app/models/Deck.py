from app import db

class Deck(db.Model):
    __tablename__ = 'decks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    
    cards = db.relationship('Card', backref='deck', lazy='dynamic') 
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}