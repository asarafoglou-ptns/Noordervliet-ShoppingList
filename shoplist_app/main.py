from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

def create_app():

  app = Flask(__name__, template_folder="templates", static_folder="static")
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
  
  db.init_app(app)

  # imports done within function to avoid circular imports
  from routes_views import register_routes
  register_routes(app, db)

  #Usually done in terminal? Only needed once?
  with app.app_context():
    db.create_all()

  return app