from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, url

class SetForm(FlaskForm):
  workoutId = IntegerField("workoutId", validators=[DataRequired()])
  reps = IntegerField("reps", validators=[DataRequired()])
  lbs = IntegerField("lbs", validators=[DataRequired()])
  submit = SubmitField("submit")
