from enum import Enum
from db import db
from models import BaseModel


autohrs_books = db.Table('autohrs_books', 
    db.Column('author_id', db.ForeignKey('authors.id')),
    db.Column('book_id', db.ForeignKey('books.id'))
)

orders_books = db.Table('buyers_books', 
    db.Column('user_id', db.ForeignKey('orders.id')),
    db.Column('book_id', db.ForeignKey('books.id'))
)

class BookModel(db.Model, BaseModel):
    __tablename__ = 'books'
    fields_to_serializer = ['id', 'title', 'price', 'isbn', 'authors']

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(230), nullable=False)
    price = db.Column(db.Float(precision=3))
    authors = db.relationship('AuthorModel', backref='books', secondary=autohrs_books)    


class OrderModel(db.Model, BaseModel):
    __tablename__ = 'orders'
    fields_to_serializer = ['id', 'title', 'payments', 'user_id', 'books']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=True)
    payments = db.relationship('PaymentModel', backref='order', lazy=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('users.id'))
    books = db.relationship('BookModel', backref='orders', secondary=orders_books)


class PaymentStatus(Enum):
    paid = 1
    not_paid = 2
    
    
class PaymentModel(db.Model, BaseModel):
    __tablename__ = 'payments'
    fields_to_serializer = ['id', 'user_id', 'order_id', 'status', 'at']

    id = db.Column(db.Integer, primary_key=True)
    at = db.Column(db.DateTime)
    status = db.Column(db.Enum(PaymentStatus))
    order_id  = db.Column(db.Integer, db.ForeignKey('orders.id'))
    user_id  = db.Column(db.Integer, db.ForeignKey('users.id'))