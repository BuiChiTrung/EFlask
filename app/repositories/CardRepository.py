from sqlalchemy import select
from app.models.Card import Card
from app.models.SystemDefinition import SystemDefinition
from app.models.UserDefinition import UserDefinition
from app.models.Word import Word

from app.repositories.BaseRepository import BaseRepository
from app import db

class CardRepository(BaseRepository): 
    def show_detail(self, card):
        if card.sys_def_id != None:
            card_detail = db.session.execute(select(Card, SystemDefinition, Word).select_from(Card).join(SystemDefinition).join(Word).filter(Card.id==card.id)).fetchone()
        elif card.user_def_id != None: 
            card_detail = db.session.execute(select(Card, UserDefinition, Word).select_from(Card).join(UserDefinition).join(Word).filter(Card.id==card.id)).fetchone()
        return card_detail