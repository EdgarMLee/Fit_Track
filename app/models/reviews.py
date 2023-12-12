from .db import db
from sqlalchemy import func

class Review(db.Model):
  __tablename__ = "reviews"

  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(500), nullable=False)
  stars = db.Column(db.Integer, nullable=False)
  userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  exerciseId = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

  created_at = db.Column("created_at", db.DateTime, default=func.now())
  updated_at = db.Column("updated_at", db.DateTime, default=func.now(), onupdate=func.now())

  exercise = db.relationship("Exercise", back_populates='reviews', foreign_keys=[exerciseId])
  user = db.relationship("User", back_populates='reviews', foreign_keys=[userId])

  def to_dict(self):
    return {
      'id': self.id,
      'exerciseId': self.exerciseId,
      'userId': self.userId,
      'user': self.user.to_dict(),
      'stars': self.stars,
      'description': self.description,
      'created_at': self.created_at
    }
