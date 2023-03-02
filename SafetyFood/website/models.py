from sqlalchemy import func
from flask_login import UserMixin
from . import db 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key =True,autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))

class Product(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key =True,autoincrement=True)
    name = db.Column(db.String(150), unique=True)
    type = db.Column(db.String(150))
    category = db.Column(db.String(150))
    wilaya = db.Column(db.String(150))
    production_qte = db.Column(db.Integer)
    consommation_qte = db.Column(db.Integer)