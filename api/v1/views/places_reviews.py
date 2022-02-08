#!/usr/bin/python3
"""palce"""

from logging import exception
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models import storage
from sqlalchemy.exc import IntegrityError


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_reviews(place_id=None):
    """retrieves the list of all Review objects"""
    all_reviews = []
    place_obj = storage.get("Place", place_id)
    if place_obj:
        for review_obj in place_obj.reviews:
            all_reviews.append(review_obj.to_dict())
        return jsonify(all_reviews)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id=None):
    """retrieves a Review object"""
    review_obj = storage.get("Review", review_id)
    if review_obj:
        return jsonify(review_obj.to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """deletes a Review object"""
    review_obj = storage.get("Review", review_id)
    if review_obj:
        storage.delete(review_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a Review object"""
    place_obj = storage.get("Place", place_id)
    try:
        obj_request = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    try:
        if place_obj:
            if obj_request:
                if 'user_id' in obj_request and 'text' in obj_request:
                    new_review_obj = Review(**obj_request)
                    setattr(new_review_obj, "place_id", place_id)
                    new_review_obj.save()
                    return (jsonify(new_review_obj.to_dict()), 201)
                else:
                    if 'user_id' not in obj_request:
                        abort(400, "Missing user_id")
                    if 'text' not in obj_request:
                        abort(400, "Missing text")
            else:
                abort(400, "Not a JSON")
        else:
            abort(404)
    except IntegrityError:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def updates_review(review_id):
    """updates a Review object"""
    review_obj = storage.get("Review", review_id)
    obj_request = request.get_json()
    if review_obj:
        if obj_request:
            for key, value in obj_request.items():
                if (key != "id" and key != "user_id" and key != "place_id" and
                        key != "created_at" and key != "updated_at"):
                    setattr(review_obj, key, value)
            review_obj.save()
            return jsonify(review_obj.to_dict())
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
