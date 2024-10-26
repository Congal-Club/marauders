from src.database import db

class Image(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  image = db.Column(db.String(200), nullable=False)
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

  def to_dict(self):
    return {"id": self.id, "image": self.image, "post_id": self.post_id}

  def __repr__(self):
    return f"Image(id={self.id}, post_id={self.post_id})"
