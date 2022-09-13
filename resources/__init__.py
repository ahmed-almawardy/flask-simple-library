from flask_restful import Resource
import abc

class GETResourceable:
    @abc.abstractmethod
    def get(self, id):
        raise NotImplementedError

class DELETEResourceable:
    @abc.abstractmethod
    def delete(self,  id):
        raise NotImplementedError

class PUTResourceable:
    @abc.abstractmethod
    def put(self,  id):
        raise NotImplementedError

class PATCHResourceable:
    @abc.abstractmethod
    def patch(self,  id):
        raise NotImplementedError

class POSTResourceable:
    @abc.abstractmethod
    def post(self):
        NotImplementedError

class Resourceable(GETResourceable, DELETEResourceable, PUTResourceable, PATCHResourceable):
    ...

class Registerable:
    @abc.abstractmethod
    def post(self):
        raise NotImplementedError()


class BaseResgister(Resource, Registerable):
    model = None

    def post(self):
        data = self.parser.parse_args()
        if self.model.get(email=data['email']):
            return {'msg': 'name/email already exists'}, 400
        model = self.model(**data)
        model.save()
        return model.serialize(), 200


class GETResource(Resource, GETResourceable):
    model = None

    def get(self, id):
        model = self.model.get(id=id)
        if not model:
            return {'msg': 'not found'}, 404
        return model.serialize()


class DELETEResource(Resource, DELETEResourceable):
    model = None
    def delete(self,  id):
        model = self.model.get(id=id)
        if not model:
            return {'msg': 'not found'}, 404
        model.delete()
        return {'msg': 'ok'}, 204


class PUTResource(Resource, PUTResourceable):
    model = None
    def put(self,  id):
        for arg in self.parser.args:
            arg.required=True
        data = self.parser.parse_args()
        model = self.model.get(id=id)
        for attr in data:
            setattr(model, attr, data[attr])
        model.save()
        return model.serialize(), 200


class PATCHResource(Resource, PATCHResourceable):
    model = None
    def patch(self,  id):
        for arg in self.parser.args:
            arg.required=False
        data = self.parser.parse_args()
        model = self.model.get(id=id)
        for attr in data:
            value = data[attr]
            if value is not None:
                setattr(model, attr, value)
        model.save()
        return model.serialize(), 200


class LISTResourceable:
    @abc.abstractmethod
    def get():
        raise NotImplementedError


class LISTResource(Resource, LISTResourceable):
    model = None

    def get(self):
        models = self.model.all()
        if models:
            return [model.serialize() for model in models], 200
        else:
            return {'msg': 'empty'}, 200 

class POSTResource(Resource, POSTResourceable):
    model = None
    parser = None
    _many_to_many_fields = []
    _one_to_many =  {}
    _local_fields = []
    
    def post(self):
        data = self.parser.parse_args()
        new_data = {}
        
        for col in data:
            if data[col] and col in self._local_fields:
                new_data[col] = data[col]
        model = self.model(**new_data)
        
        for col in data:
            if col in self._one_to_many:
                for_model = self._one_to_many[col].get(id=data[col])
                setattr(model, col, for_model)

        for col in self._many_to_many_fields:
            relation = getattr(model, col)
            relation.append(data[col])

        
        model.save()
        

        return  model.serialize(), 200

class GRUDResource(GETResource, DELETEResource,PUTResource,PATCHResource,Resourceable):
    ...
