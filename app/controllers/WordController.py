import random

from flask import Blueprint, request
from flask_login import login_required

from app import db
from app.repositories.WordRepository import WordRepository
from app.util import google_translate, json_response, list_to_json_array

repository = WordRepository('app.models.Word', 'Word')
word_blueprint = Blueprint('word_blueprint', __name__)

@word_blueprint.route('/')
@login_required
def find_like():
    words = repository.find_like(request.args.get('word'))
    result = []
    
    for word in words:
        result.append(get_word_defs_and_convert_to_dict(word))

    return json_response(True, result)

@word_blueprint.route('/<id>')
def show(id):
    word = repository.show(id)
    if hasattr(word, 'vi_mean') == False:
        repository.update(word.id, {'vi_meaning': google_translate(word.word)})
    
    word = get_word_defs_and_convert_to_dict(word)
    return json_response(True, word)

@word_blueprint.route('/random')
def get_random_words():
    quantity = request.args.get('quantity')
    TOTAL_WORDS = 48190
    
    if int(quantity) > TOTAL_WORDS:
        return json_response(False, 'Invalid quantity', 400)
    
    random_word_ids = random.sample(range(1, TOTAL_WORDS), int(quantity))
    
    result = []
    for id in random_word_ids:
        word = repository.show(id)
        result.append(get_word_defs_and_convert_to_dict(word))
    
    return json_response(True, result)


def get_word_defs_and_convert_to_dict(word):
    defs = word.sys_defs.all()
    word = word.as_dict()
    word['sys_defs'] = list_to_json_array(defs)
    
    return word