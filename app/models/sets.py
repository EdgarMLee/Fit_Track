from .db import db

class Set(db.Model):
  __tablename__ = 'sets'

  id = db.Column(db.Integer, primary_key=True)
  workoutId = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
  reps = db.Column(db.Integer, nullable=False)
  lbs = db.Column(db.Integer, nullable=False)

  def to_dict(self):
    return {
      'id': self.id,
      'workoutId': self.workoutId,
      'reps': self.reps,
      'lbs': self.lbs
    }
