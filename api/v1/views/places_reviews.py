#!/usr/bin/python3
"""creates a new view for Review objects"""
from api.v1.views import app_views
from models.user import User
from models.place import Place
from models.review import Review
from models import storage
from flask import json, jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=["GET"],
                 strict_slashes=False)
def reviews(place_id):
    """retrieves the list of all review objects of a place object"""
    placeobj = storage.get(Place, place_id)
    if placeobj is None:
        abort(404)
    new_list = []
    for obj in placeobj:
        if obj.place_id == place_id:
            new_list.append(obj.to_dict())
    return jsonify(new_list)


@app_views.route('/reviews/<review_id>', methods=["GET"],
                 strict_slashes=False)
def review_id(review_id):
    """retrieves a review object"""
    try:
        reviewobj = storage.get(Review, review_id).to_dict()
        return jsonify(reviewobj)
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=["DELETE"],
                 strict_slashes=False)
def review_delete(review_id):
    """deletes a review object"""
    reviewobj = storage.get(Review, review_id)
    if reviewobj is not None:
        reviewobj.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=["POST"],
                 strict_slashes=False)
def review_create(place_id):
    """creates a review object"""
    body_dict = request.get_json()
    allplaces = storage.get(Place, place_id)
    if allplaces is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in body_dict:
        abort(400, "Missing user_id")
    if storage.get(User, body_dict["user_id"]) is None:
        abort(404)
    if "text" not in body_dict:
        abort(400, "Missing text")
    reviewobj = Review(**body_dict)
    reviewobj.save()
    return jsonify(reviewobj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["PUT"],
                 strict_slashes=False)
def review_update(review_id):
    """updates existing review object"""
    reviewobj = storage.get(Review, review_id)
    if reviewobj is None:
        abort(404)
    body_dict = request.get_json()
    if body_dict is None:
        abort(400, "Not a JSON")
    body_dict.pop("id", None)
    body_dict.pop("user_id", None)
    body_dict.pop("place_id", None)
    body_dict.pop("created_at", None)
    body_dict.pop("updated_at", None)
    for key, value in body_dict.items():
        setattr(reviewobj, key, value)
    reviewobj.save()
    return jsonify(reviewobj.to_dict()), 200
