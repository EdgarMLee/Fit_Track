from .db import db

class Workout(db.Model):
  __tablename__ = 'workouts'

  id = db.Column(db.Integer, primary_key=True)
  planId = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
  exerciseId = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
  setId = db.Column(db.Integer, db.ForeignKey('sets.id'), nullable=False)
  completed = db.Column(db.Boolean, nullable=False)

  set = db.relationship('Set', back_populates='workouts', foreign_keys=[setId])
  exercise = db.relationship("Exercise", back_populates='workouts', foreign_keys=[exerciseId])

  def to_dict(self):
    return {
      'id': self.id,
      'planId': self.planId,
      'exerciseId': self.exerciseId,
      'setId': self.setId,
      'completed': self.completed,
      'set': self.set.to_dict(),
      'planId': self.planId,
    }
