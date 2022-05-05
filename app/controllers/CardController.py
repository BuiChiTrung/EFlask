from datetime import datetime

from flask import Blueprint, request
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired

from app.repositories.BaseRepository import BaseRepository
from app.util import json_response

card_blueprint = Blueprint('card_blueprint', __name__)
repository = BaseRepository('app.models.Card', 'Card')
deck_repository = BaseRepository('app.models.Deck', 'Deck')
sys_def_repository = BaseRepository('app.models.SystemDefinition', 'SystemDefinition')

class CreateCardForm(FlaskForm):
    sys_def_id = IntegerField(validators=[DataRequired()])
    deck_id = IntegerField(validators=[DataRequired()])

@card_blueprint.route('/', methods=['POST'])
@login_required
def store():
    form = CreateCardForm(request.form, meta={'csrf': False})
    if form.validate_on_submit():
        # new_deck = repository.store({'name': form.name.data, 'user_id': current_user.id})
        return json_response(True, 123, 200)
    return json_response(False, form.errors, 400)
    # print('ajdl;asjdl;asjdfl;ksjdfl;kasjdfl;aksjdf')
    # new_card = {
    #     'sys_def_id': request.form.sys_def_id.data, 
    #     'deck_id': request.form.deck_id.data, 
    #     'due_time': datetime.now(), 
    #     'interval': 1, 
    #     'e_factor': 2
    # }
    
    # print(new_card, 'aslkdj;alskdfj;alskdhf')
    
    # if (sys_def_repository.show(new_card['sys_def_id']) == None or 
    #     deck_repository.belong_to_current_user(new_card['deck_id']) == False):
    #     return json_response(False, 'Add card fail')
    
    # card = repository.store(card)
    return json_response(True, {}, 201)

@card_blueprint.route('/<id>')
@login_required
def show(id):
    card = repository.show(id)
    return json_response(True, {})