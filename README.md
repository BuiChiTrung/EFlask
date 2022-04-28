# Backend installation

### Create virtual env & install dependencies

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Add env var

```
export FLASK_APP=eflask.py
export FLASK_DEBUG=true
export FLASK_RUN_PORT=5001
```

### Setup DB
Create db EFlask in mysql, then:
```
flask shell
db.create_all()
```
Add data from file to db
```
python -m build_db.add_words_to_db
```

### Migrate database (when db schema changes)

```
flask db init
flask db migrate
flask db upgrade
```

### Run 

```
flask run
```