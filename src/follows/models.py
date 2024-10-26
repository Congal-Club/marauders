from src.database import db

class Follow(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_following = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user_followed = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def to_dict(self):
    return {"id": self.id, "user_following": self.user_following, "user_followed": self.user_followed}

  def __repr__(self):
    return f"Follow(follower_id={self.user_following}, followed_id={self.user_followed})"
