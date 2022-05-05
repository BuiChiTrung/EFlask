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
    

@deck_blueprint.route('/', methods=['POST'])
@login_required
def store():
    form = CreateDeckForm(request.form, meta={'csrf': False})
    if form.validate_on_submit():
        new_deck = repository.store({'name': form.name.data, 'user_id': current_user.id})
        return json_response(True, new_deck.as_dict())
    return json_response(False, form.errors, 400)

@deck_blueprint.route('/<id>')
def show(id):
    deck = repository.show(id)
    if deck == None:
        return json_response(False, 'Deck not found', 400)
    if deck.user_id != current_user.id:
        return json_response(False, 'This deck doesn\'t belong to you', 403)

    result = repository.show_cards_detail(id)
    print(result)
    return json_response(True, deck.as_dict())

@deck_blueprint.route('/<id>', methods=['PUT'])
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

