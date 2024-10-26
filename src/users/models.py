from src.database import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  lastName = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(200), nullable=False)
  image = db.Column(db.String(200))

  posts = db.relationship('Post', backref='user', lazy=True)
  comments = db.relationship('Comment', backref='user', lazy=True)
  followed = db.relationship('Follow', foreign_keys='Follow.user_following', backref='follower', lazy=True)
  followers = db.relationship('Follow', foreign_keys='Follow.user_followed', backref='followed', lazy=True)

  def to_dict(self):
    return {"id": self.id, "name": self.name, "lastName": self.lastName, "email": self.email, "image": self.image}

  def __repr__(self):
    return f"User(name={self.name}, email={self.email})"
