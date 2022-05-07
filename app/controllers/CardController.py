from datetime import datetime
from functools import wraps

from flask import Blueprint, request
from flask_login import login_required, current_user

from app.repositories.CardRepository import CardRepository
from app.repositories.DeckRepository import DeckRepository
from app.util import json_response, tuple_to_dict

card_blueprint = Blueprint('card_blueprint', __name__)
repository = CardRepository('app.models.Card', 'Card')
deck_repository = DeckRepository('app.models.Deck', 'Deck')


def verifyCardOwner(func):
    @wraps(func)
    def inner(id):
        card = repository.show(id)
        if card == None:
            return json_response(False, 'Card doesn\'t exist', 400)
        print(card.deck.user_id)
        if card.deck.user_id != current_user.id:
            return json_response(False, 'This card doesn\'t belong to you', 403)
        card = card.as_dict()
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
    pass
    # print(card)
    # if card['sys_def_id'] != None:
    # return json_response(True, card)
    
@card_blueprint.route('/<id>', methods=['DELETE'])
@verifyCardOwner
@login_required
def delete(card):
    deleted_card = repository.destroy(card['id'])
    return json_response(True, deleted_card.as_dict())
