from app import db

class UserDefinition(db.Model):
    __tablename__ = 'user_definitions'

    id = db.Column(db.Integer, primary_key=True)
    meaning = db.Column(db.String(1000), nullable=False)
    lexical_category = db.Column(db.String(15))
    example = db.Column(db.String(1000))

    word_id = db.Column(db.Integer, db.ForeignKey('words.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    cards = db.relationship('Card', backref='user_def', lazy='dynamic')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return (f'<"meaning": "{self.meaning}",'
                f'"lexical_category": "{self.lexical_category}",'
                f'"example": "{self.example}",'
                f'"word_id": "{self.word_id}"'
                '>')