from flask import Blueprint, request, jsonify
from app.models import db, Plan, Workout, Exercise, Review, Set
from ..forms.plan_form import PlanForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages

plan_routes = Blueprint("plans", __name__, url_prefix="/plans")

#Get all Plans
@plan_routes.route("")
def all_plans():
    #Query for all plans
    plans = Plan.query.all()
    #Create an array that stores list of plan dictionaries directly
    #Appends to array in loop
    planarr = [plan.to_dict() for plan in plans]
    #Return JSON response with list of plan dictionaries
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
        plan_dict = plan.to_dict()
        # planId = plan.to_dict()["id"]
        # image = db.session.query(Image).filter(Image.planId == planId).first()
        # image = db.session.query(Image).filter(Image.planId == planId).[1]
        # ^ Input that once you added seeder data to image for 2nd image
        # if image:
        #     plan["image"] = image.to_dict()
        #Append plan to array
        planarr.append(plan_dict)
    return {"plans": planarr}

#Get all Plans by current user
@plan_routes.route("/current")
@login_required
def get_current():
    #Query for plans that belong to owner
    plans = Plan.query.filter(Plan.owner_id == current_user.id).all()
    #Return JSON response with each plan (object) converted to dictionary
    return {"plans": [plan.to_dict() for plan in plans]}

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

#Delete Plan
@plan_routes.route("/<int:plan_id>", methods=['DELETE'])
@login_required
def delete_plan(plan_id):
    #Query to get plan by ID
    plan = Plan.query.get(plan_id)
    #Authorization step to ensure only owner can delete plan
    if plan.owner_id == current_user.id:
        #Delete and save changes to database
        db.session.delete(plan)
        db.session.commit()
        #Response message with status code after deletion
        return {
                "message": "Plan successfully deleted",
                "status-code": 200
        }, 200
    else:
        #Unauthorized user error
        return {"errors": "Unauthorized User"}, 401

#Search a Plan
@plan_routes.route("/search")
def search_plan():
    #Query for value of "name" paramter from request's query string
    query_name = request.args.get("name")
    #Case-insensitive search filter on "name" column of Plan model
    #ilike is a partial match function using query string
    plans = Plan.query.filter(Plan.name.ilike(f"%{query_name}%")).all()
    #Return searched results as JSON response
    return {
        "plans": [plan.to_dict() for plan in plans]
    }
