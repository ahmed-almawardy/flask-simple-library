import abc
from db import db 

class ModelInterface:
    @abc.abstractclassmethod
    def _get(cls, **kwargs):
        raise NotImplemented('need a body')
    
    @abc.abstractclassmethod
    def get(cls, **kwargs):
        raise NotImplemented('need a body')
    
    @abc.abstractclassmethod
    def all(cls, **kwargs):
        raise NotImplemented('need a body')
    
    @abc.abstractmethod
    def serialize(self):
        raise NotImplemented('need a body')

    @abc.abstractmethod
    def save(self):
        raise NotImplemented('need a body')

    @abc.abstractmethod
    def delete(self):
        raise NotImplemented('need a body')


class BaseModel(ModelInterface):
    fields_to_serializer = ['id']
    _many_to_many_fields_serializer = {}
    
    @classmethod
    def _get(cls, **kwargs):
        return cls.query.filter_by(**kwargs)
    
    @classmethod
    def get(cls, **kwargs):
        models = cls._get(**kwargs)
        if models:
            return models.first()
    
    @classmethod    
    def all(cls, **kwargs):
        return cls.query.all()

    def serialize(self):
        output = {}
        for field in self.fields_to_serializer:
            value = getattr(self, str(field))
            output[field] = value
        
        for field in self._many_to_many_fields_serializer:
            value = getattr(self, str(field))
            value = [{'id': row.id} for row in value]
            output[field] = value
        return output

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
