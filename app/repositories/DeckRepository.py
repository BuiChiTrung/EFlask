from flask_login import current_user
from sqlalchemy import select, join

from app import db
from app.models.Card import Card
from app.models.Word import Word
from app.models.SystemDefinition import SystemDefinition    
from app.repositories.BaseRepository import BaseRepository

class DeckRepository(BaseRepository): 
    def show_cards_detail(self, id):
        return db.session.execute(select(self.class_, Card, SystemDefinition, Word).select_from(self.class_).join(Card).join(SystemDefinition).join(Word).filter_by(id=id)).all()
    
    def belong_to_current_user(self, id):
        deck = self.show(id)
        return deck != None and deck.user_id == current_user.id