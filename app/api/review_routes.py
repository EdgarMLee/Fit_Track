from flask import Blueprint, request, jsonify
from app.models import db, Plan, Workout, Exercise, Review, Set
from ..forms.plan_form import PlanForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages

review_routes = Blueprint("reviews", __name__, url_prefix="/reviews")

#Get all Reviews
@review_routes.route("/")
def all_reviews():
    #Query to get all reviews
    reviews = Review.query.all()
    #Array of plan ID from review loop
    plan_ids = [review.planId for review in reviews]
    #Query to get all plan names for all reviews
    plans = Plan.query.filter(Plan.id.in_(plan_ids)).all()
    #Dictionary with planID key associated with plan name
    plan_dict = {plan.id: plan.to_dict()["name"] for plan in plans}
    #Initialize empty array to store converted object to dictionaries
    reviewarr = []
    for review in reviews:
        review_dict = review.to_dict()
        #Adds name of associated plan to dictionary
        review_dict["plan"] = plan_dict.get(review.planId)
        reviewarr.append(review_dict)
    #Return JSON response
    return {"reviews": reviewarr}

#Get review by ID
@review_routes.route("/<int:id>")
def get_review(id):
    #Query review based on ID
    review = Review.query.get(id)
    #Return review convert to dictionary from object
    return review.to_dict()
