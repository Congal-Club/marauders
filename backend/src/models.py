from .database import db

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

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  images = db.relationship('Image', backref='post', lazy=True)
  comments = db.relationship('Comment', backref='post', lazy=True)

  def to_dict(self):
    return {"id": self.id, "content": self.content, "user_id": self.user_id}

  def __repr__(self):
    return f"Post(id={self.id}, content={self.content})"

class Image(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  image = db.Column(db.String(200), nullable=False)
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

  def to_dict(self):
    return {"id": self.id, "image": self.image, "post_id": self.post_id}

  def __repr__(self):
    return f"Image(id={self.id}, post_id={self.post_id})"

class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  comment = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

  def to_dict(self):
    return {"id": self.id, "comment": self.comment, "user_id": self.user_id, "post_id": self.post_id}

  def __repr__(self):
    return f"Comment(id={self.id}, comment={self.comment})"

class Follow(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_following = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user_followed = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def to_dict(self):
    return {"id": self.id, "user_following": self.user_following, "user_followed": self.user_followed}

  def __repr__(self):
    return f"Follow(follower_id={self.user_following}, followed_id={self.user_followed})"
