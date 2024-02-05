#!/usr/bin/python3
"""RESTful API view to handle actions for 'Review' objects"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"],
                 strict_slashes=False)
def place_reviews_routes(place_id):
    """
    GET: Retrieves the list of all Review objects in the place where
         id == place_id
    POST: Creates a Review object in the place where id == place_id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == "GET":
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    elif request.method == "POST":
        in_data = request.get_json(silent=True)
        if in_data is None or not isinstance(in_data, dict):
            return 'Not a JSON\n', 400

        user_id = in_data.get("user_id")
        if user_id is None:
            return "Missing user_id\n", 400

        user = storage.get(User, user_id)
        if user is None:
            abort(404)

        text = in_data.get("text")
        if text is None:
            return "Missing text\n", 400

        in_data["place_id"] = place_id
        review = Review(**in_data)
        review.save()
        return review.to_dict(), 201


@app_views.route("/reviews/<review_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def review_id_routes(review_id):
    """
    GET: Retrieves the Review where id == review_id
    PUT: Updates the Review that has id == review_id
    DELETE: Deletes the Review that has id == review_id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == "GET":
        return jsonify(review.to_dict())

    elif request.method == "PUT":
        in_data = request.get_json(silent=True)
        if in_data is None or not isinstance(in_data, dict):
            return 'Not a JSON\n', 400

        for key, val in in_data.items():
            if key not in ["id", "user_id", "place_id", "created_at",
                           "updated_at"]:
                setattr(review, key, val)
        review.save()
        return review.to_dict(), 200

    elif request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
