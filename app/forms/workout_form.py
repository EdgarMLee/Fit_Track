from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, url

class WorkoutForm(FlaskForm):
  planId = IntegerField("planId", validators=[DataRequired()])
  exerciseId = IntegerField("exerciseId", validators=[DataRequired()])
  setId = IntegerField("setId", validators=[DataRequired()])
  completed = SelectField("completed", validators=[DataRequired()])
  submit = SubmitField("submit")
