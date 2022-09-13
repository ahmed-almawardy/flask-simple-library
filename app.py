from flask import Flask
from flask_restful import  Api
from flask_jwt_extended import JWTManager
from db import db
from resources.core import Book, Books, Order, Orders, Payment, Payments
from resources.user import Author, Authors, User, UserLogin, UserRegister, Users
from flask_migrate import Migrate


app = Flask(__name__)
# hardcoded for simplisity
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:secret@localhost:5432/test_db"
# disable Flask-SqlAlchemy extension feature
# allowing the main sqlalchemy library to do the job instead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '$so_secure-key@'
app.secret_key = 'so-secret-key-from-env'

api = Api(app)
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()
 

# @jwt.user_claims_loader
# def add_user_claims(identity):
    # user = UserModel.get(id=identity.user_id)
    # if user and user.is_admin:
        # return {'is_admin': True}
    # else:
        # return {'is_admin': False}



api.add_resource(User, '/api/users/<int:id>/')
api.add_resource(UserRegister, '/api/users/')
api.add_resource(Users, '/api/users/')
api.add_resource(UserLogin, '/api/users/login/')
api.add_resource(Author, '/api/authors/<int:id>')
api.add_resource(Authors, '/api/authors/')
api.add_resource(Books, '/api/books/')
api.add_resource(Book, '/api/books/<int:id>/')
api.add_resource(Orders, '/api/orders/')
api.add_resource(Order, '/api/orders/<int:id>/')
api.add_resource(Payments, '/api/payments/')
api.add_resource(Payment, '/api/payments/<int:id>/')




if __name__ == '__main__':
    app.run(5000,debug=True)