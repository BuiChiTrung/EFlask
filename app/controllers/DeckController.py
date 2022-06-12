from flask import Blueprint,  request
from flask_login import login_required, current_user
from app.repositories.CardRepository import CardRepository

from app.util.others import json_response, list_to_json_array
from app.repositories.DeckRepository import DeckRepository

from functools import wraps

repository = DeckRepository('app.models.Deck', 'Deck')
card_repository = CardRepository('app.models.Card', 'Card')
deck_blueprint = Blueprint('deck_blueprint', __name__)
    
def verifyDeckOwner(func):
    @wraps(func)
    def inner(id):
        deck = repository.show(id)
        if deck == None:
            return json_response(False, 'Deck not found', 400)
        if deck.user_id != current_user.id:
            return json_response(False, 'This deck doesn\'t belong to you', 403)
        res = func(deck.as_dict())
        return res
    return inner
    

@deck_blueprint.route('', methods=['POST'])
@login_required
def store():
    if 'name' not in request.form or len(request.form['name']) < 1:
        return json_response(False, "Deck name is required", 400)
    elif len(repository.find({'name': request.form['name']})) > 0:
        return json_response(False, "Deck name already exists", 400)
    else:
        new_deck = repository.store({'name': request.form['name'], 'user_id': current_user.id})
        return json_response(True, new_deck.as_dict(), 201)   


@deck_blueprint.route('/<id>')
@login_required
@verifyDeckOwner
def show(deck):
    deck['cards'] = []
    
    get_only_due_card = False
    if request.args.get('card-type') == 'due':
        get_only_due_card = True
    
    cards = repository.show_cards_detail(deck['id'], get_only_due_card)
    print(cards)
    for i in range (len(cards)):
        card = {}
        card.update(cards[i][0].as_dict())
        sys_def = cards[i][1].as_dict()
        del sys_def["id"]
        word = cards[i][2].as_dict()
        del word["id"]
        
        card.update(sys_def)
        card.update(word)
        
        del card['deck_id']
        deck['cards'].append(card)
            
    return json_response(True, deck)


@deck_blueprint.route('/<id>', methods=['PUT'])
@login_required
@verifyDeckOwner
def update(deck):
    if 'name' in request.form:
        repository.update(deck['id'], {'name': request.form["name"]})
    return json_response(True, deck)


@deck_blueprint.route('/<id>', methods = ['DELETE'])
@login_required
@verifyDeckOwner
def destroy(deck):
    deleted_deck = repository.destroy(deck['id'])
    return json_response(True, deleted_deck.as_dict())


@deck_blueprint.route('/')
@login_required
def show_user_decks():
    return json_response(True, list_to_json_array(current_user.decks.all()))