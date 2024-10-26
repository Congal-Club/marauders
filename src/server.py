from flask import Flask
from src.database import db

def create_app():
  app = Flask(__name__)
  
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marauders.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  
  db.init_app(app)

  with app.app_context():
    db.create_all()

  return app
