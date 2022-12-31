#!/usr/bin/python3
''' cities.py'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET", "POST"],
                 strict_slashes=False)
def get_reviews(place_id):
    '''Retrieves the list of all Review objects of a Place'''
    place_object = storage.get(Place, place_id)
    if not place_object:
        abort(404)

    if request.method == "GET":
        reviews = [review.to_dict() for review in place_object.reviews]
        return jsonify(reviews)

    elif request.method == "POST":
        if not request.is_json:
            abort(400, description="Not a JSON")

        if "text" not in request.json:
            abort(400, description="Missing text")

        if "user_id" not in request.json:
            abort(400, description="Missing user_id")

        review_json = request.get_json()

        user = storage.get(User, review_json["user_id"])
        if not user:
            abort(404)

        review_obj = Review(user_id=review_json["user_id"],
                            place_id=place_id,
                            **review_json)
        storage.new(review_obj)
        storage.save()

        return jsonify(review_obj.to_dict()), 201


@app_views.route("/reviews/<review_id>",
                 methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_review_id(review_id):
    '''Retrieves a Review object'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == "GET":
        return jsonify(review.to_dict())

    elif request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        if not request.is_json:
            abort(400, description="Not a JSON")

        review_json = request.get_json()
        not_needed = ["id", "created_at", "updated_at", "user_id", "place_id"]
        for attr, attr_value in review_json.items():
            if attr not in not_needed:
                setattr(review, attr, attr_value)
        review.save()
        return jsonify(review.to_dict()), 200
