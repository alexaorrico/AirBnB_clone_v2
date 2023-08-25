#!/usr/bin/python3#!/usr/bin/python3
"""reviews view module"""
from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
    "/places/<place_id>/reviews", methods=["GET", "POST"], strict_slashes=False
)
def reviews_from_place_id(place_id):
    """returns all reviews of place or 404"""
    place = storage.get(Place, place_id)
    if request.method == "GET":
        if place is None:
            abort(404)
        reviews_list = []
        for review, review_details in storage.all(Review).items():
            review = review_details.to_dict()
            if review["place_id"] == str(place_id):
                reviews_list.append(review)
        if reviews_list is not None:
            return jsonify(reviews_list)

    if request.method == "POST":
        # If not valid JSON, error 400
        if place is None:
            abort(404)
        request_data = request.get_json()
        if request_data is None:
            abort(400, "Not a JSON")
        if "text" not in request_data:
            abort(400, "Missing text")
        if "user_id" not in request_data:
            abort(400, "Missing user_id")
        request_data["place_id"] = place_id
        user = storage.get(User, request_data.get("user_id"))
        if user is None:
            abort(404)
        newReview = Review(**request_data)
        newReview.save()
        return jsonify(newReview.to_dict()), 201


@app_views.route(
    "/reviews/<review_id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False
)
def review_from_id(review_id):
    """returns review from id"""
    # GET, DELETE, PUT both need storage.get(Review), so do it once for all
    review = storage.get(Review, review_id)
    if request.method == "GET":
        if review is None:
            abort(404)
        return jsonify(review.to_dict())

    if request.method == "DELETE":
        if review is None:
            abort(404)
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == "PUT":
        if review is None:
            abort(404)
        try:
            request_data = request.get_json()
            request_data.pop("id", None)
            request_data.pop("place_id", None)
            request_data.pop("created_at", None)
            request_data.pop("updated_at", None)
            request_data.pop("user_id", None)
            for key in request_data.keys():
                setattr(review, key, request_data[key])
            review.save()
            return jsonify(review.to_dict()), 200

        except Exception:
            return "Not a JSON\n", 400
