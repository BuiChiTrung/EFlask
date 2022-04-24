from sqlalchemy import table
from app import db

class SystemDefinition(db.Model):
    __tablename__ = 'system_definitions'

    id = db.Column(db.Integer, primary_key=True)
    meaning = db.Column(db.String(100), nullable=False)
    lexical_category = db.Column(db.String(15))
    example = db.Column(db.String(150))

    word_id = db.Column(db.Integer, db.ForeignKey('words.id'))

    def __repr__(self):
        return (f'<"meaning": "{self.meaning}",'
                f'"lexical_category": "{self.lexical_category}",'
                f'"example": "{self.example}",'
                f'"word_id": "{self.word_id}"'
                '>')