#!/usr/bin/python3

"""Handles all default RESTFul API actions for review_object"""

from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<string:place_id>/reviews", methods=["GET", "POST"])
def place_review(place_id):
    """handles GET, POST  RESTFul API actions"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
        return

    if request.method == "GET":
        reviews = []
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)

    elif request.method == "POST":
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        elif "user_id" not in request.get_json():
            return make_response(jsonify({"error": "Missing user_id"}), 400)
        user = storage.get(User, request.get_json()["user_id"])
        if user is None:
            abort(404)
            return
        elif "text" not in request.get_json():
            return make_response(jsonify({"error": "Missing text"}), 400)
        new_dict = request.get_json()
        new_dict["place_id"] = place_id
        new_review = Review(**new_dict)
        new_review.save()
        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["GET", "PUT", "DELETE"])
def review(review_id):
    """handles GET, PUT, DELETE  RESTFul API actions on review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
        return

    if request.method == "GET":
        return jsonify(review.to_dict())

    elif request.method == "DELETE":
        review.delete()
        storage.save()
        return jsonify({})

    elif request.method == "PUT":
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        updates = request.get_json()
        for attr, value in updates.items():
            if attr not in ["id", "user_id", "place_id", "created_at",
                            "updated_at"]:
                setattr(review, attr, value)
        review.save()
        return make_response(jsonify(review.to_dict()), 200)
