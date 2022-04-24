import json

from app import create_app, db
from app.models.SystemDefinition import SystemDefinition
from app.models.Word import Word

app = create_app()
db.init_app(app)

INVALID_WORD = 'Word not found'
WORD_DETAIL = 'build_db/words_detail.txt'
WORD_IMAGE = 'build_db/words_image_url'

def add_word_detail(start_line, end_line):
    for i in range(start_line, end_line):
        word = json.loads(lines[i])
        if 'error' in word: continue
        
        definitions = word['definitions']
        del word['definitions']
        
        new_word = Word(**word)
        db.session.add(new_word)

        for definition in definitions:
            db.session.add(SystemDefinition(**definition, word=new_word))    
        
    db.session.commit()

def add_word_image(start_line, end_line):        
    for i in range(start_line, end_line):
        word = json.loads(lines[i])
        if word['img_url'] != None:
            exist_word = Word.query.filter_by(word=word['word']).first()
            exist_word['img_url'] = word['img_url']
            db.sessions.add(exist_word)

    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        with open(WORD_DETAIL, 'r') as inp:
            lines = inp.readlines()
            add_word_detail(0, len(lines))
        with open(WORD_IMAGE, 'r') as inp:
            lines = inp.readlines()
            add_word_image(0, len(lines))