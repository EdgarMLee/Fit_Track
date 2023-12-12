from .db import db

class Exercise(db.Model):
  __tablename__ = "exercises"

  id = db.Column(db.Integer, primary_key=True)

  name = db.Column(db.String(50), nullable=False)
  primarymuscle = db.Column(db.String(50), nullable=False)
  secondarymuscle = db.Column(db.String(50), nullable=False)


  # user = db.relationship('User', back_populates='exercise', foreign_keys=[owner_id])
  reviews = db.relationship("Review", back_populates="exercise", cascade="all, delete")
  images = db.relationship("Image", back_populates="exercise", cascade="all, delete")

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "primarymuscle": self.primarymuscle,
      "secondarymuscle": self.secondarymuscle,
      # "owner_id": self.owner_id,
      "review_ids": [review.id for review in self.reviews],
      "image_ids": [image.id for image in self.images],
    }
