from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

def create_app():
"""
Function that creates/initializes the webapplication. Takes no arguments and returns app; the webapplication
Usage: should be called to in the run file with flask_app = create_app()
"""

  #Configure the app and initialize the database
  app = Flask(__name__, template_folder="templates", static_folder="static")
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
  app.config["SECRET_KEY"] = "secret-key"
  
  db.init_app(app)

  #Define the login manager system
  login_manager = LoginManager()
  login_manager.init_app(app)

  from models import User

  @login_manager.user_loader
  def load_user(id):
    """
    Defines how the login manager loads the user, in this case by user id.
    :param id: user id
    :return: user information from database
    """
    return User.query.get(id
  
  bcrypt = Bcrypt(app)

  # imports done within function to avoid circular imports
  from routes import register_routes
  register_routes(app, db, bcrypt)

  #Creates the database with the model class tables
  with app.app_context():
    db.create_all()

  return app





