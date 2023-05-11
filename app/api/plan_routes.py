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

#Get plan by ID
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
