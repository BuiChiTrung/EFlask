from email.policy import default
from app import db

class Card(db.Model):
    __tablename__ = 'cards'
    
    id = db.Column(db.BigInteger, primary_key=True)
    due_time = db.Column(db.DateTime, nullable=False, index=True)
    interval = db.Column(db.Float, default=1)
    e_factor = db.Column(db.Float, default=1.3)
    
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id'))
    sys_def_id = db.Column(db.Integer, db.ForeignKey('system_definitions.id'), unique=True)
    user_def_id = db.Column(db.Integer, db.ForeignKey('user_definitions.id'), unique=True)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}