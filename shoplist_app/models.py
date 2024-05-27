from main import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    

    def __repr__(self):
        return f"Username: {self.username}, Email: {self.email}"
    
class Staple(db.Model):
    __tablename__ = "staples"
    
    id = db.Column(db.Integer, primary_key=True)
    staple = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Pantry Staple: {self.staple}"
    
class ShoppingItem(db.Model):
    __tablename__ = "shopping_list"
    
    id = db.Column(db.Integer, primary_key=True)
    shopping_item = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Shopping List Item: {self.shopping_item}"