import importlib
import logging

from sqlalchemy import update

from app import db
from app.models.Deck import Deck


class BaseRepository:
    def __init__(self, module, class_name):
        self.class_ = getattr(importlib.import_module(module), class_name)

    def store(self, record):
        model_instance = self.class_(**record)
        db.session.add(model_instance)
        db.session.commit()
        return model_instance

    def show(self, id):
        return self.class_.query.get(id)

    def update(self, id, attrs):
        db.session.execute(update(self.class_).filter_by(id=id).values(**attrs))
        db.session.commit()

    def destroy(self, id):
        model_instance = self.class_.query.get(id)
        db.session.delete(model_instance)
        db.session.commit()
        return model_instance
    
    def find(self, attrs):
        return self.class_.query.filter_by(**attrs).all()
        