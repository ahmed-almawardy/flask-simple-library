from datetime import datetime
from flask_restful import reqparse
from models.core import PaymentModel
from models.core import BookModel, OrderModel
from models.user import UserModel
from resources import GRUDResource, LISTResource, POSTResource


class Books(LISTResource, POSTResource):
    model = BookModel
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True)
    parser.add_argument('price', type=float, required=True)
    parser.add_argument('isbn', type=str, required=True)
    parser.add_argument('authors', type=list[int], required=False)


class Book(GRUDResource):
    model = BookModel
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str,  nullable=False)
    parser.add_argument('price', type=float,  nullable=False)
    parser.add_argument('isbn', type=str,   nullable=False)
    parser.add_argument('authors', type=list[int], required=False)


class Orders(LISTResource, POSTResource):
    model = OrderModel
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, nullable=False)
    parser.add_argument('payments', type=list[int], required=False, nullable=True)
    parser.add_argument('user_id', type=int, required=True, nullable=False)
    parser.add_argument('books', type=int, required=True, action='append', nullable=False)
    _one_to_many = {'user_id': UserModel,}
    _many_to_many_fields ={'books': BookModel,'payment': PaymentModel}

class Order(GRUDResource):
    model = OrderModel
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=int, required=False, nullable=False)
    parser.add_argument('payments', type=list, required=False, nullable=True)
    parser.add_argument('user_id', type=int, required=False, nullable=False)
    parser.add_argument('books', type=int, required=False, nullable=True)
    _one_to_many = {'user_id': UserModel,}
    _many_to_many_fields ={'books': BookModel,'payment': PaymentModel}


class Payments(LISTResource):
    model = PaymentModel
    parser = reqparse.RequestParser()
    parser.add_argument('user', type=int, required=True, nullable=False)
    parser.add_argument('order', type=int, required=True, nullable=False)
    parser.add_argument('status', type=int, required=True, nullable=False)
    parser.add_argument('at', type=datetime, required=True, nullable=False)


class Payment(GRUDResource):
    model = PaymentModel
    parser = reqparse.RequestParser()
    parser.add_argument('user', type=int, required=True, nullable=False)
    parser.add_argument('order', type=int, required=True, nullable=False)
    parser.add_argument('status', type=int, required=True, nullable=False)
    parser.add_argument('at', type=datetime, required=True, nullable=False)
