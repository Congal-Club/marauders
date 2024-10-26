from src.database import db

class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  comment = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

  def to_dict(self):
    return {"id": self.id, "comment": self.comment, "user_id": self.user_id, "post_id": self.post_id}

  def __repr__(self):
    return f"Comment(id={self.id}, comment={self.comment})"
