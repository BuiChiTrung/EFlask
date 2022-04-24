from flask import Blueprint, jsonify, request

from app import db
from app.models.Word import Word

word_blueprint = Blueprint('word_blueprint', __name__)

@word_blueprint.route('/words')
def index():
    word = Word.query.filter_by(word=request.args.get('word')).first()
    sys_defs = word.sys_defs.all()

    defs = []
    for sys_def in sys_defs:
        defs.append(sys_def.as_dict())

    return jsonify({
        "word": word.as_dict(),
        "defs": defs
    })

@word_blueprint.route('/words/<id>')
def show(id):
    word = Word.query.get(id)
    return jsonify(word.as_dict())

