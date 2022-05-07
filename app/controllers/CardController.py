from datetime import datetime

from flask import Blueprint, request
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired

from app.repositories.CardRepository import CardRepository
from app.repositories.DeckRepository import DeckRepository
from app.repositories.SystemDefinitionRepository import SystemDefinitionRepository
from app.util import json_response

card_blueprint = Blueprint('card_blueprint', __name__)
repository = CardRepository('app.models.Card', 'Card')
deck_repository = DeckRepository('app.models.Deck', 'Deck')
sys_def_repository = SystemDefinitionRepository('app.models.SystemDefinition', 'SystemDefinition')


@card_blueprint.route('/', methods=['POST'])
@login_required
def store():
    new_card = {
        'sys_def_id': request.form['sys_def_id'], 
        'deck_id': request.form['deck_id'], 
        'due_time': datetime.now(), 
        'interval': 1, 
        'e_factor': 2
    }
    
    if (repository.find({'id': new_card['deck_id'], 'sys_def_id': new_card['sys_def_id']}) != [] or 
        deck_repository.belong_to_current_user(new_card['deck_id']) == False):
        return json_response(False, 'Add card fail', 400)
    
    new_card = repository.store(new_card)
    return json_response(True, new_card.as_dict(), 201)


@card_blueprint.route('/<id>')
@login_required
def show(id):
    card = repository.show(id)
    return json_response(True, {})

