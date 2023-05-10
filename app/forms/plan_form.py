from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, url

class PlanForm(FlaskForm):
  owner_id = IntegerField("owner_id", validators=[DataRequired()])
  name = StringField("name", validators=[DataRequired()])
  private = SelectField("private", validators=[DataRequired()])
  time = IntegerField("time", validators=[DataRequired()])
  exercises = SelectField("exercises", validators=[DataRequired()])
  workouts = SelectField("workouts", validators=[DataRequired()])
  submit = SubmitField("submit")
