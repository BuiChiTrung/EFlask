class Base():
    exclude_fields = []
    
    def as_dict(self):
        res = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for field in self.exclude_fields:
            if field in res:
                del res[field]
        return res
    
    # def __repr__(self):
    #     return str({c.name: getattr(self, c.name) for c in self.__table__.columns})
    