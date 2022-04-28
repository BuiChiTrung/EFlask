from flask import Blueprint, jsonify, request
from flask_login import login_required

from app import db
from app.repositories.WordRepository import WordRepository

repository = WordRepository('app.models.Word', 'Word')
word_blueprint = Blueprint('word_blueprint', __name__)

@word_blueprint.route('/')
@login_required
def find_like():
    words = repository.find_like(request.args.get('word'))
    result = []
    
    for word in words:
        defs = word.sys_defs.all()
        for i in range(len(defs)):
            defs[i] = defs[i].as_dict()
        word = word.as_dict()
        word['sys_defs'] = defs
        result.append(word)

    return jsonify(result)

@word_blueprint.route('/<id>')
def show(id):
    return jsonify(repository.show(id).as_dict())

