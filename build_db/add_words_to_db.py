import json

from app import create_app, db
from app.models.SystemDefinition import SystemDefinition
from app.models.Word import Word

app = create_app()
db.init_app(app)

INVALID_WORD = 'Word not found'
WORD_DETAIL = 'build_db/words_detail.txt'
WORD_IMAGE = 'build_db/words_image_url.txt'

def add_word_detail(start_line, end_line):
    max_len = 0
    for i in range(start_line, end_line):
        line = json.loads(lines[i])
        if 'error' in line: continue
        if Word.query.filter_by(word=line['word']).first() != None: continue
        
        definitions = line['definitions']
        del line['definitions']
        
        new_word = Word(**line)
        db.session.add(new_word)


        for definition in definitions:
            # if 'example' in definition:
            #     max_len = max(max_len, len(definition['example']))
            db.session.add(SystemDefinition(**definition, word=new_word))    
        
    db.session.commit()
    # print(max_len)

def add_word_image(start_line, end_line):        
    for i in range(start_line, end_line):
        print(i)
        line = json.loads(lines[i])
        if line['img_url'] != None:
            word = Word.query.filter_by(word=line['word']).first()
            if word == None: continue

            word.img_url = line['img_url']
            db.session.add(word)

    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        with open(WORD_DETAIL, 'r') as inp:
            lines = inp.readlines()
            add_word_detail(0, len(lines))
        with open(WORD_IMAGE, 'r') as inp:
            lines = inp.readlines()
            add_word_image(0, len(lines))