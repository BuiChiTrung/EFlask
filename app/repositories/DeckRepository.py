from datetime import datetime
from flask_login import current_user
from sqlalchemy import select

from app import db
from app.models.Card import Card
from app.models.Word import Word
from app.models.SystemDefinition import SystemDefinition    
from app.models.UserDefinition import UserDefinition
from app.repositories.BaseRepository import BaseRepository

class DeckRepository(BaseRepository): 
    def show_cards_detail(self, id, get_only_due_card):
        date_filter = datetime(2001, 2, 5)
        if get_only_due_card:
            date_filter = datetime.now()
        
        result = []
        result.extend(list(
            db.session.execute(
                select(Card, SystemDefinition, Word)
                .select_from(Card)
                .join(SystemDefinition)
                .join(Word)
                .filter(Card.deck_id == id)
                .filter(Card.due_time <= date_filter))
            .all()
        ))
        
        result.extend(list(
            db.session.execute(
                select(Card, UserDefinition, Word)
                .select_from(Card)
                .join(UserDefinition)
                .join(Word)
                .filter(Card.deck_id == id)
                .filter(Card.due_time <= date_filter))
            .all()
        ))
        return result
    
    def belong_to_current_user(self, id):
        deck = self.show(id)
        return deck != None and deck.user_id == current_user.id