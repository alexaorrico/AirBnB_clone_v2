#!/usr/bin/python3
"""
Create a new view for Review object that
handles all default RESTFul API actions:
"""
from models import storage
from models.place import Place
from models.review import Review
from flask import abort
from flask import request
from flask.json import jsonify
from api.v1.views import app_views
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_from_place(place_id=None):
    """
    Retrieves the list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    info = []
    if place is not None:
        for review in place.reviews:
            info.append(review.to_dict())
        return jsonify(info)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    """
    Retrieves a Review object
    """
    review = storage.get(Review, review_id)
    if review is not None:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id=None):
    """
    Deletes a Review object
    """
    review = storage.get(Review, review_id)
    if review is not None:
        review.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id=None):
    """
    Creates a Review
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json = request.get_json(silent=True)
    if "user_id" not in json:
        abort(400, "Missing user_id")
    if json is None:
        abort(400, "Not a JSON")
    user = storage.get(User, json.get('user_id'))
    if user is None:
        abort(404)
    if 'text' not in json:
        abort(400, "Missing text")
    review = Review(**json)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """
    Updates a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")
    for key, value in json.items():
        if key != 'updated_at' and key != 'created_at' and \
                        key != 'id' and key != 'user_id' and key != 'place_id':
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
