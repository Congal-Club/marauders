from flask import Flask, send_from_directory
import os

from .database import db
from .views import UserRoutes, AuthRoutes, PostRoutes, CommentRoutes, FollowRoutes, LikeRoutes, ImageRoutes

def create_app():
  app = Flask(__name__)
  
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marauders.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
  os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

  @app.route('/uploads/<filename>')
  def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
  
  db.init_app(app)
  
  user_routes = UserRoutes()
  auth_routes = AuthRoutes()
  post_routes = PostRoutes()
  comment_routes = CommentRoutes()
  follow_routes = FollowRoutes()
  like_routes = LikeRoutes()
  image_routes = ImageRoutes()

  app.register_blueprint(user_routes.blueprint, url_prefix='/api')
  app.register_blueprint(auth_routes.blueprint, url_prefix='/api')
  app.register_blueprint(post_routes.blueprint, url_prefix='/api')
  app.register_blueprint(comment_routes.blueprint, url_prefix='/api')
  app.register_blueprint(follow_routes.blueprint, url_prefix='/api')
  app.register_blueprint(like_routes.blueprint, url_prefix='/api')
  app.register_blueprint(image_routes.blueprint, url_prefix='/api')
  
  with app.app_context():
    db.create_all()

  return app
