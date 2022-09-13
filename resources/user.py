from flask_restful import Resource
from flask_restful import reqparse
from models.user import AuthorModel, UserModel
from flask_jwt_extended import create_access_token, create_refresh_token
from resources import BaseResgister, GRUDResource, LISTResource


class Users(LISTResource):
    model = UserModel


class UserRegister(BaseResgister):
    mdoel = UserModel
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help='name to regiter with', required=True)
    parser.add_argument('email', type=str, help='email to regiter with', required=True)
    parser.add_argument('password', type=str, help='password to regiter with', required=True)


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help='Email to login')
    parser.add_argument('password', type=str, required=True, help='Password to login')
    
    def post(self):
        data = self.parser.parse_args()
        user = UserModel.get(email=data['email'])
        if user.validate_password(data['password']):
            return { **user.serialize(), 'access_token': create_access_token(identity=user.id), "refresh_token": create_refresh_token(identity=user.id)}
        return {'msg': "invalid credintionals"}, 400


class User(GRUDResource):
    model = UserModel
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, help='user email', nullable=False)
    parser.add_argument('name', type=str, help='user name', nullable=False)
    parser.add_argument('password', type=str, help='user password', nullable=False)


class Author(GRUDResource):
    model = AuthorModel
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, help='author email', nullable=False)
    parser.add_argument('name', type=str, help='author name', nullable=False)


class Authors(BaseResgister, LISTResource):
    model = AuthorModel
