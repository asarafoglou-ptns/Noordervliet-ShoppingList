from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

def create_app():

  app = Flask(__name__, template_folder="templates", static_folder="static")
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
  app.config["SECRET_KEY"] = "secret-key"
  
  db.init_app(app)

  login_manager = LoginManager()
  login_manager.init_app(app)

  from models import User

  #Defines how the login manager loads the user
  @login_manager.user_loader
  def load_user(id):
      return User.query.get(id)
  
  bcrypt = Bcrypt(app)

  # imports done within function to avoid circular imports
  from routes import register_routes
  register_routes(app, db, bcrypt)

  #Usually done in terminal? Only needed once?
  with app.app_context():
    db.create_all()

  return app





