from flask_migrate import Migrate

from app import create_app, db
from app.models.SystemDefinition import SystemDefinition
from app.models.Word import Word
from app.models.User import User

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, Word=Word, SystemDefinition=SystemDefinition, User=User)