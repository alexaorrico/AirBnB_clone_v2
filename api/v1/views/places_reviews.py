#!/usr/bin/python3
""" new view for Review object that handles all default RestFul API actions """
import os
import json
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review_id(review_id):
    """ Retrieves a Review object """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_review_id(review_id):
    """ Deletes a Review object """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_reviews(place_id):
    """ Creates a Review """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    my_request = request.get_json()
    if not my_request:
        abort(400, "Not a JSON")
    if "user_id" not in my_request:
        abort(400, "Missing user_id")
    user_id = my_request['user_id']
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    if "text" not in my_request:
        abort(400, "Missing text")
    review = Review(**my_request)
    setattr(review, "place_id", place_id)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def put_review_id(review_id):
    """ Updates a Review object """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    my_request = request.get_json()
    if not my_request:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in my_request.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
