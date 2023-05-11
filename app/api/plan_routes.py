from flask import Blueprint, request, jsonify
from app.models import db, Plan, Workout, Exercise, Review, Set, Image
from ..forms.plan_form import PlanForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages

plan_routes = Blueprint("plans", __name__, url_prefix="/plans")

#Get all Plans
@plan_routes.route("")
def all_plans():
    #Query for all plans
    plans = Plan.query.all()
    #Empty array to store queried plans
    planarr = []
    if plans is not None:
        #If plans exists, create loop and convert object to dictionary
        for plan in plans:
            plan = plan.to_dict()
            # planId = plan.to_dict()["id"]
            # image = db.session.query(Image).filter(Image.planId == planId).first()
            # if image:
            #     plan['image'] = image.to_dict()
            #append dictionary to array
            planarr.append(plan)
    #Return as a json response
    return {"plans": planarr}

#Get Plan by ID
@plan_routes.route("/<int:id>")
def get_plan(id):
    #Query for plan based on ID
    plan = Plan.query.get(id)
    #Empty array to store queried plan
    planarr = []
    #If plan exists, convert object to dictionary
    if plan is not None:
        plan = plan.to_dict()
        # planId = plan.to_dict()["id"]
        # image = db.session.query(Image).filter(Image.planId == planId).first()
        # image = db.session.query(Image).filter(Image.planId == planId).[1]
        # ^ Input that once you added seeder data to image for 2nd image
        # if image:
        #     plan["image"] = image.to_dict()
        #Append plan to array
        planarr.append(plan)
    return plan

#Create a Plan
@plan_routes.route("/", methods=["POST"])
@login_required
def create_plan():
    #Create instance of PlanForm class
    form = PlanForm()
    #Sets CSRF Token in form as security to prevent cross-site request forgery attacks
    form["csrf_token"].data = request.cookies["csrf_token"]
    #Queries for all exercises from database
    exercises = Exercise.query.all()
    #Sets choices for exercise form
    form.exercise.choices=[(exercise.to_exercise(), exercise.to_exercisename()) for exercise in exercises]
    if form.validate_on_submit():
        new_plan = Plan(
            #Input fields with info
            owner_id=current_user.id,
            name=form.name.data,
            private=form.private.data,
            time=form.time.data,
            exercises=form.exercises.data,
            workouts=form.workouts.data
        )
        #Add and save changes to database
        db.session.add(new_plan)
        db.session.commit()
        #Return jsonified data with successful status
        return jsonify(new_plan.to_dict()), 200
    else:
        return {"errors": validation_errors_to_error_messages(form.errors)}, 401

#Edit a Plan
@plan_routes.route("/<int:plan_id>", methods=["PUT"])
@login_required
def edit_plan(plan_id):
  #Create instance of PlanForm class
  form = PlanForm()
  #Sets CSRF Token in form as security to prevent cross-site request forgery attacks
  form["csrf_token"].data = request.cookies["csrf_token"]
  #Queries for all exercises from database
  exercises = Exercise.query.all()
  #Sets choices for exercise form
  form.exercise.choices=[(exercise.to_exercise(), exercise.to_exercisename()) for exercise in exercises]
  if form.validate_on_submit():
      #Queries for plan based on plan ID
      plan = Plan.query.get(plan_id)
      #Authorization to check if plan belongs to owner before allowing update
      if plan.owner_id == current_user.id:
          plan.name = form.name.data
          plan.private = form.private.data
          plan.time = form.time.data
          plan.exercises = form.exercises.data
          plan.workouts = form.workouts.data
          #Save changes to database
          db.session.commit()
          #Returns updated plan as JSON with status code 204
          return jsonify(plan.to_dict()), 204
      else:
          #If current user is not authorized to modify plan
          return {"errors": "Unauthorized"}, 401
  else:
      return {"errors": validation_errors_to_error_messages(form.errors)}, 401
