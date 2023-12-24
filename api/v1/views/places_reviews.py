#!/usr/bin/python3
"""
    this module contains flask app routes
        flask APP routes:
        methods:
            GET:
                /places/<place_id>/reviews:
                    list all place reviews using place ID
                /reviews/<review_id>:
                    display a review dictionary using ID
            DELETE:
                /reviews/<review_id>:
                    delete a review using ID
            POST:
                /places/<place_id>/reviews:
                    create a new review to place using place ID
            PUT:
                /reviews/<review_id>:
                    update a review object using ID
"""

from api.v1.views import app_views
from flask import abort, jsonify, request

# import all needed models
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_place_reviews(place_id):
    """display all reviews of a place using the 'place_id'"""
    if (storage.get(Place, place_id)) is None:
        abort(404)
    reviews_list = []
    [reviews_list.append(review.to_dict())
     for review in storage.all(Review).values()
     if review.place_id == place_id]
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """display a review using ID"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    return obj.to_dict()


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def remove_review(review_id):
    """remove a review using ID"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """create a new place review using the 'place_id'"""
    if (storage.get(Place, place_id)) is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    if (storage.get(User, (request.get_json())["user_id"])) is None:
        abort(404)
    if "text" not in request.get_json():
        return jsonify({"error": "Missing text"}), 400
    obj_dict = request.get_json()
    obj_dict["place_id"] = place_id
    obj = Review(**obj_dict)
    obj.save()
    return obj.to_dict(), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """update a review instance using ID"""
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    [setattr(obj, key, value) for key, value in request.get_json().items()
     if key not in ignore_keys]
    obj.save()
    return obj.to_dict(), 200
