from flask_login import  UserMixin
from main import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    staples = db.relationship('Staple', backref='user', lazy=True)
    groceries = db.relationship('Grocery', backref='user', lazy=True)

    def __repr__(self):
        return f'<Username: {self.username}, Email: {self.email}>'
    
    def get_id(self):
        return self.id
    
class Staple(db.Model):
    __tablename__ = "staples"
    
    id = db.Column(db.Integer, primary_key=True)
    staple = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Pantry Staple: {self.staple}"
    
class Grocery(db.Model):
    __tablename__ = "shopping_list"
    
    id = db.Column(db.Integer, primary_key=True)
    grocery = db.Column(db.String(50))
    was_staple = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Shopping List Item: {self.grocery}"