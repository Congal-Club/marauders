from src.database import db

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
  