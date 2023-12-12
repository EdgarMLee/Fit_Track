from flask import Blueprint, request, jsonify
from app.models import db, Plan, Workout, Exercise, Review, Set
from ..forms.plan_form import PlanForm
from ..forms.review_form import ReviewForm
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

#Get review by current user
@review_routes.route("/current")
@login_required
def get_current():
    reviews = (
    #Query from database for review
    db.session.query(Review)
    .join(Plan)
    #Retrive all review based on user
    .filter_by(userId=current_user.id)
    .all()
)
    #Array containing review based on ID
    plan_ids = [review.planId for review in reviews]
    #Query filtering out plans
    plans = Plan.query.filter(Plan.id.in_(plan_ids)).all()
    #Create dictionary with id as key and name for plans
    plan_dict = {plan.id: plan.to_dict()["name"] for plan in plans}
    reviewarr = []
    for review in reviews:
        review_dict = review.to_dict()
        review_dict["plan"] = plan_dict.get(review.planId)
        reviewarr.append(review_dict)
    return {"reviews": reviewarr}

# Create Review
@review_routes.route("", methods=['POST'])
@login_required
def create_review():
    # Directly access the JSON data using request.json
    data = request.json
    new_review = Review(
        exerciseId=data.get('exerciseId'),
        userId=data.get('userId'),
        stars=data.get('stars'),
        description=data.get('description')
    )
    form = ReviewForm()
    # Flask's get_json() to retrieve from JSON payload
    # Safer approach
    form['csrf_token'].data = request.get_json().get('csrf_token')

    if form.validate_on_submit():
        db.session.add(new_review)
        db.session.commit()
        return jsonify(new_review.to_dict()), 201
    else:
        return {"errors": validation_errors_to_error_messages(form.errors)}, 400

# Update Review
@review_routes.route("/<int:id>", methods=["PATCH"])
@login_required
def update_review(id):
    form = ReviewForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        #Query to retrive single review that belongs to specific iD
        review = Review.query.get(id)
        #Authorization condition if ID belongs to the user
        if review.userId == current_user.id:
            review.description = form.description.data
            review.stars = form.stars.data
            db.session.commit()
            return jsonify(review.to_dict()), 200
        else:
            return {"errors": 'Unauthorized'}, 403
    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 400
