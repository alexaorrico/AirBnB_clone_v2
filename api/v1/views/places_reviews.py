#!/usr/bin/python3
"""
This module contains the views for Review objects
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def reviews_by_place(place_id):
    """retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews
                    if review.place_id == place_id])


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """retrieves a Review object using its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a new Review object"""
    data = request.get_json(silent=True)
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    user_id = data.get('user_id')
    if not user_id:
        abort(400, "Missing user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not data.get('text'):
        abort(400, "Missing text")
    data.update({'place_id': place_id})
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """updates a Review object"""
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for key, value in data.items():
        if key not in ignore:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict())
