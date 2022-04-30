from app import db

class Card(db.Model):
    __tablename__ = 'cards'
    
    id = db.Column(db.BigInteger, primary_key=True)
    due_time = db.Column(db.DateTime, nullable=False)
    interval = db.Column(db.Float, nullable=False)
    e_factor = db.Column(db.Float, nullable=False)
    
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id', ondelete='CASCADE', onupdate='CASCADE'))
    sys_def_id = db.Column(db.Integer, db.ForeignKey('system_definitions.id', ondelete='CASCADE', onupdate='CASCADE'))
    user_def_id = db.Column(db.Integer, db.ForeignKey('user_definitions.id', ondelete='CASCADE', onupdate='CASCADE'))
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}