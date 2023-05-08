from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, url

class ReviewForm(FlaskForm):
  stars = IntegerField("stars", validators=[DataRequired(), NumberRange(1,5)])
  description = StringField("description", validators=[DataRequired()])
  userId = IntegerField("userId", validators=[DataRequired()])
  exerciseId = IntegerField("exerciseId", validators=[DataRequired()])
  submit = SubmitField("submit")
