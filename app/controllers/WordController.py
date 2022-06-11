from flask import Blueprint, jsonify, request
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
        defs = word.sys_defs.all()
        word = word.as_dict()
        word['sys_defs'] = list_to_json_array(defs)
        result.append(word)

    return json_response(True, result)

@word_blueprint.route('/<id>')
def show(id):
    word = repository.show(id)
    if hasattr(word, 'vi_mean') == False:
        repository.update(word.id, {'vi_meaning': google_translate(word.word)})
    
    defs = word.sys_defs.all()
    word = word.as_dict()
    word['sys_defs'] = list_to_json_array(defs)

    return json_response(True, word)