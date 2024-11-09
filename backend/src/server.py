from flask import Flask
from .database import db
from .views import UserRoutes

def create_app():
  app = Flask(__name__)
  
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marauders.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  
  db.init_app(app)
  
  user_routes = UserRoutes()
  app.register_blueprint(user_routes.blueprint, url_prefix='/api')
  
  with app.app_context():
    db.create_all()

  return app
