from db import db
from hashlib import sha256
from models import BaseModel


class UserModel(db.Model, BaseModel):
    __tablename__ = 'users'
    fields_to_serializer = ['id', 'name', 'email']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True, index=True)
    password = db.Column(db.String(250), nullable=False)
    orders = db.relationship('OrderModel', backref='user')
    payments = db.relationship('PaymentModel', backref='user')


    def validate_password(self, password):
        return sha256(bytes(password, encoding='utf-8')).hexdigest() == self.password

    def save(self):
        self.password = sha256(bytes(self.password, encoding='utf-8')).hexdigest()
        db.session.add(self)
        db.session.commit()


class AuthorModel(db.Model, BaseModel):
    __tablename__ = 'authors'
    fields_to_serializer = ['id', 'name', 'email']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=True)