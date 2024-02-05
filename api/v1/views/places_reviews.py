#!/usr/bin/python3
"""This module contains the view for the place resource."""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route(
        "/places/<place_id>/reviews",
        strict_slashes=False,
        methods=["GET", "POST"]
        )
def get_reviews(place_id):
    """ Function to get the reviws
    of a place_id"""
    place_object = storage.get(Place, place_id)
    if place_object is None:
        abort(404)
    if request.method == "GET":
        return jsonify(
                [obj.to_dict() for obj in place_object.reviews]
                )
    if request.method == "POST":
        if not request.is_json:
            abort(400, "Not a JSON")
        json_data = request.get_json()
        if "user_id" not in json_data:
            abort(400, "Missing user_id")
        reviewer_user_object = storage.get(User, json_data["user_id"])
        if reviewer_user_object is None:
            abort(404)
        if "text" not in json_data:
            abort(400, "Missing text")
        new_review_object = Review(**json_data)
        storage.new(new_review_object)
        storage.save()
        return jsonify(new_review_object.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>",
        strict_slashes=False,
        methods=["GET", "DELETE", "PUT"]
        )
def get_review(review_id):
    """Function to get a particular review using
    review_id from the list of reviews"""
    review_object = storage.get(Review, review_id)
    if not review_object:
        abort(404)
    if request.method == "GET":
        return jsonify(review_object.to_dict())
    if request.method == "DELETE":
        storage.delete(review_object)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        if not request.is_json:
            abort(400, "Not a JSON")
        json_data = request.get_json()
        for key, value in json_data:
            if key not in [
                    "id", "user_id", "place_id",
                    "created_at", "updated_at"
                        ]:
                setattr(review_object, key, value)
        review_object.save()
        #  storage.save()
        return jsonify(review_object.to_dict()), 200
