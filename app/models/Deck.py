from app import db

class Deck(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50))
    
    