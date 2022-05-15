from flask_migrate import Migrate
from sqlalchemy import select, update, insert

from app import create_app, db
from app.models.Card import Card
from app.models.Deck import Deck
from app.models.SystemDefinition import SystemDefinition
from app.models.UserDefinition import UserDefinition
from app.models.Word import Word
from app.models.User import User

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, 
                insert=insert, select=select, update=update,
                Word=Word, 
                SystemDefinition=SystemDefinition, 
                User=User, Deck=Deck, 
                UserDefinition=UserDefinition, 
                Card=Card)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)