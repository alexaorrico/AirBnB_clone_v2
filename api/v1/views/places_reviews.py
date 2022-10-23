#!/usr/bin/python3
"""route for reviews"""
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from flask import abort, jsonify, request, make_response


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET", "POST"])
def get_place_review(place_id):
    """retrieves the list of all Review objects of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "GET":
        all_place_reviews = []
        for review in place.reviews:
            all_place_reviews.append(review.to_dict())
        return jsonify(all_place_reviews)
    elif request.method == "POST":
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        if "user_id" not in data.keys():
            abort(400, description="Missing user_id")
        if not storage.get(User, data["user_id"]):
            abort(404)
        if "text" not in data.keys():
            abort(400, description="Missing text")
        new = Review(**data)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def a_review(review_id):
    """Retrieves,Deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    elif request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        try:
            data = request.get_json()
            if not data:
                abort(400, description="Not a JSON")
        except Exception:
            abort(400, description="Not a JSON")
        for attr, val in data.items():
            if attr not in ["id", "user_id", "place_id", "created_at",
                            "updated_at"]:
                setattr(review, attr, val)
        return jsonify(review.to_dict()), 200
