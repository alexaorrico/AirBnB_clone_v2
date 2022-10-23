#!/usr/bin/python3
""" A Review object that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('places/<place_id>/reviews',
                 method=['GET'], strict_slashes=False)
def get_all_reviews(place_id=None):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = storage.all("Review")
    reviews_list = []
    for value in reviews.values():
        if value.place_id == place_id:
            reviews_list.append(value.to_dict())
    return jsonify(reviews_list)


@app_views.route('reviews/<review_id>', method=['GET'], strict_slashes=False)
def get_review(review_id=None):
    """Retrieves a Review object"""
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('reviews/<review_id>',
                 method=['DELETE'], strict_slashes=False)
def delete_review(review_id=None):
    """Deletes a Review object"""
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('<places/place_id>/reviews',
                 method=['POST'], strict_slashes=False)
def create_review(place_id=None):
    """Creates a Review"""
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in args:
        return jsonify({"error": "Missing user_id"}), 400
    elif "text" not in args:
        return jsonify({"error": "Missing text"}), 400
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    user_id = args["user_id"]
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    args["place_id"] = place_id
    obj = Review(**args)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('reviews/<review_id>', method=['PUT'], strict_slashes=False)
def update_review(review_id=None):
    """Updates a Review object"""
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not A JSON"}), 400
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    for key, value in args.items():
        if key not in ["id", "place_id", "user_id",
                       "updated_at", "created_at"]:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
