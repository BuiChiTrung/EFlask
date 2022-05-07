from datetime import datetime
from functools import wraps

from flask import Blueprint, request
from flask_login import login_required, current_user

from app.repositories.CardRepository import CardRepository
from app.repositories.DeckRepository import DeckRepository
from app.repositories.SystemDefinitionRepository import SystemDefinitionRepository
from app.repositories.UserDefinitionRepository import UserDefinitionRepository
from app.util import json_response, tuple_to_dict

card_blueprint = Blueprint('card_blueprint', __name__)
repository = CardRepository('app.models.Card', 'Card')
deck_repository = DeckRepository('app.models.Deck', 'Deck')
user_def_repository = UserDefinitionRepository('app.models.UserDefinition', 'UserDefinition')
sys_def_repository = SystemDefinitionRepository('app.models.SystemDefinition', 'SystemDefinition')


def verifyCardOwner(func):
    @wraps(func)
    def inner(id):
        card = repository.show(id)
        if card == None:
            return json_response(False, 'Card doesn\'t exist', 400)
        print(card.deck.user_id)
        if card.deck.user_id != current_user.id:
            return json_response(False, 'This card doesn\'t belong to you', 403)
        return func(card)
    
    return inner


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
    
    if repository.find({'id': new_card['deck_id'], 'sys_def_id': new_card['sys_def_id']}) != []:
        return json_response(False, 'Card already exist', 400)
    if deck_repository.belong_to_current_user(new_card['deck_id']) == False:
        return json_response(False, 'This deck doesn\'t belong to you', 400)
        
    
    new_card = repository.store(new_card)
    return json_response(True, new_card.as_dict(), 201)


@card_blueprint.route('/<id>')
@verifyCardOwner
@login_required
def show(card):
    card_detail = repository.show_detail(card)
    return json_response(True, tuple_to_dict(card_detail))


@card_blueprint.route('/<id>', methods=['PUT'])
@verifyCardOwner
@login_required
def update(card):
    new_definition = {}
    if 'meaning' in request.form: new_definition['meaning'] = request.form['meaning']
    if 'lexical_category' in request.form: new_definition['lexical_category'] = request.form['lexical_category']
    if 'example' in request.form: new_definition['example'] = request.form['example']
    
    if card.sys_def_id != None:
        new_definition['word_id'] = card.sys_def.word_id
        user_definition = user_def_repository.store(new_definition)
        card = repository.update(card.id, {'sys_def_id': None, 'user_def_id': user_definition.id}).as_dict()
    else: 
        user_definition = user_def_repository.update(card.user_def_id, new_definition)
        
    return json_response(True, card.as_dict())
    
    
@card_blueprint.route('/<id>', methods=['DELETE'])
@verifyCardOwner
@login_required
def delete(card):
    deleted_card = repository.destroy(card.id)
    return json_response(True, deleted_card.as_dict())
