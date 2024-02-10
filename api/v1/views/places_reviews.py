#!/usr/bin/python3
"""
view for Review objects that handles all default RestFul API actions
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_reviews(place_id):
    """Retrieves the list of all Review objects or
    create a new Review object"""
    place_obj = storage.get("Place", place_id)
    if place_obj:
        if request.method == 'GET':
            return jsonify([review_obj.to_dict() for review_obj in place_obj.
                            reviews]), 200
        if request.method == 'POST':
            if not request.get_json(silent=True):
                abort(400, "Not a JSON")
            if not request.get_json(silent=True).get('user_id'):
                abort(400, "Missing user_id")
            user_obj = storage.get("User", request.get_json(silent=True).
                                   get('user_id'))
            if not user_obj:
                abort(404)
            if not request.get_json(silent=True).get('text'):
                abort(400, "Missing text")
            kwargs = request.get_json(silent=True)
            new_review = Review(**kwargs)
            setattr(new_review, 'place_id', place_id)
            new_review.save()
            return jsonify(new_review.to_dict()), 201
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review_byid(review_id):
    """Retrieves a Review object by id, delete or update a Review object"""
    review_obj = storage.get("Review", review_id)
    if review_obj:
        if request.method == 'GET':
            return jsonify(review_obj.to_dict()), 200
        elif request.method == 'DELETE':
            storage.delete(review_obj)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            if not request.get_json(silent=True):
                abort(400, "Not a JSON")
            kwargs = request.get_json(silent=True)
            if kwargs:
                for key, value in kwargs.items():
                    if key not in ["id", "user_id", "place_id", "created_at",
                                   "updated_at"]:
                        setattr(review_obj, key, value)
                review_obj.save()
            return jsonify(review_obj.to_dict()), 200
    else:
        abort(404)
