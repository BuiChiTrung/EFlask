from app import db
import importlib

class BaseRepository:
    def __init__(self, module, class_name):
        self.class_ = getattr(importlib.import_module(module), class_name)

    def create(self, record):
        model_instace = self.class_(**record)
        db.session.add(model_instace)
        db.session.commit()

    def show(self, id):
        return self.class_.query.get(id)
    
    def find(self, attrs):
        return self.class_.query.filter_by(**attrs).all()
        