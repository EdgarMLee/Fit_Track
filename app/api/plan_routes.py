from flask import Blueprint, request, jsonify
from app.models import db, Plan, Workout, Exercise, Review, Set, Image
from ..forms.plan_form import PlanForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages

plan_routes = Blueprint("plans", __name__, url_prefix="/plans")

#Get all Plans
@plan_routes.route("")
def all_plans():
    plans = Plan.query.all()
    planarr = []
    if plans is not None:
        for plan in plans:
            plan = plan.to_dict()
            # planId = plan.to_dict()["id"]
            # image = db.session.query(Image).filter(Image.planId == planId).first()
            # if image:
            #     plan['image'] = image.to_dict()
            planarr.append(plan)
    return {"plans": planarr}

#Get Plan by ID
@plan_routes.route("/<int:id>")
def get_plan(id):
    plan = Plan.query.get(id)
    planarr = []
    if plan is not None:
        plan = plan.to_dict()
        # planId = plan.to_dict()["id"]
        # image = db.session.query(Image).filter(Image.planId == planId).first()
        # image = db.session.query(Image).filter(Image.planId == planId).[1]
        # ^ Input that once you added seeder data to image for 2nd image
        # if image:
        #     plan["image"] = image.to_dict()
        planarr.append(plan)
    return plan

#Create a Plan
@plan_routes.route("/", methods=["POST"])
@login_required
def create_plan():
    form = PlanForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    exercises = Exercise.query.all()
    form.exercise.choices=[(exercise.to_exercise(), exercise.to_exercisename()) for exercise in exercises]
    if form.validate_on_submit():
        new_plan = Plan(
            owner_id=current_user.id,
            name=form.name.data,
            private=form.private.data,
            time=form.time.data,
            exercises=form.exercises.data,
            workouts=form.workouts.data
        )
        db.session.add(new_plan)
        db.session.commit()
        return jsonify(new_plan.to_dict()), 200
    else:
        return {"errors": validation_errors_to_error_messages(form.errors)}, 401

