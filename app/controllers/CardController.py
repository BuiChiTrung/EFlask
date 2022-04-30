from datetime import datetime

from flask import Blueprint

from app.repositories.BaseRepository import BaseRepository
from app.util import json_response

card_blueprint = Blueprint('card_blueprint', __name__)
repository = BaseRepository('app.models.UserDefinition', 'UserDefinition')
repository = BaseRepository('app.models.Card', 'Card')

@card_blueprint.route('/', methods = ['POST'])
def store():
    card = {'sys_def_id': 1, 'deck_id': 1, 'due_time': datetime(2022, 4, 29), 'interval': 1, 'e_factor': 2}
    card = repository.store(card)
    return json_response(True, card.as_dict())