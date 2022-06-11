source venv/bin/activate
export FLASK_APP=eflask.py
flask db init
flask db migrate
flask db upgrade