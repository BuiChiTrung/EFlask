# Backend installation

### Create virtual env & install dependencies

```
python3 -m venv venv
pip install -r requirements.txt
```

### Migrate database

```
flask db init
flask db migrate
flask db upgrade
```

### Add env var

```
export FLASK_APP=eflask.py
export FLASK_DEBUG=true
export FLASK_RUN_PORT=5001
```

### Run 

```
flask run
```