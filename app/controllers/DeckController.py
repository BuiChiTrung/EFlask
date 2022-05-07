from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from app.util import json_response
from app.repositories.DeckRepository import DeckRepository

repository = DeckRepository('app.models.Deck', 'Deck')
deck_blueprint = Blueprint('deck_blueprint', __name__)

class CreateDeckForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    
def verifyDeckOwner(func):
    def inner(id):
        deck = repository.show(id)
        if deck == None:
            return json_response(False, 'Deck not found', 400)
        if deck.user_id != current_user.id:
            return json_response(False, 'This deck doesn\'t belong to you', 403)
        res = func(deck)
        return res
    return inner
    

@deck_blueprint.route('/', methods=['POST'])
@login_required
def store():
    form = CreateDeckForm(request.form, meta={'csrf': False})
    if form.validate_on_submit():
        new_deck = repository.store({'name': form.name.data, 'user_id': current_user.id})
        return json_response(True, new_deck.as_dict(), 201)
    return json_response(False, form.errors, 400)


@deck_blueprint.route('/<id>')
@verifyDeckOwner
@login_required
def show(deck):
    deck = deck.as_dict()
    deck['cards'] = []
    cards = repository.show_cards_detail(deck['id'])
    print(cards)
    for i in range (len(cards)):
        card = {}
        card.update(cards[i][0].as_dict())
        card.update(cards[i][1].as_dict())
        card.update(cards[i][2].as_dict())
        
        del card['deck_id']
        deck['cards'].append(card)
            
    return json_response(True, deck)


@deck_blueprint.route('/<id>', methods=['PUT'])
@login_required
def update(id):
    deck = repository.show(id)
    if deck == None:
        return json_response(False, 'Deck not found', 400)
    if deck.user_id != current_user.id:
        return json_response(False, 'This deck doesn\'t belong to you', 403)
    
    if 'name' in request.form:
        repository.update(id, {'name': request.form["name"]})
    return json_response(True, deck.as_dict())


@deck_blueprint.route('/<id>', methods = ['DELETE'])
@login_required
def destroy(id):
    deck = repository.show(id)
    if deck == None:
        return json_response(False, 'Deck not exist', 400)
    if deck.user_id != current_user.id:
        return json_response(False, 'This deck doesn\'t belong to you', 403)
    
    deleted_deck = repository.destroy(id)
    return json_response(True, deleted_deck.as_dict())

