from .db import db

class Plan(db.Model):
  __tablename__ = "plans"

  id = db.Column(db.Integer, primary_key=True)
  owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

  name = db.Column(db.String(50), nullable=False)
  workouts = db.Column(db.String(100), nullable=False)
  private = db.Column(db.Boolean, nullable=False)
  time = db.Column(db.Integer, nullable=False)

  user = db.relationship('User', back_populates='plan', foreign_keys=[owner_id])
  exercises = db.relationship('Exercise', back_populates='plan', cascade='all, delete')
  workouts = db.relationship('Workout', back_populates='plan', cascade='all, delete')

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "workouts": self.workouts,
      "private": self.private,
      "time": self.time
    }
