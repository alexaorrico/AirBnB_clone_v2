#!/usr/bin/python3
"""
script that starts a Flask web application:
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, place
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews_all(place_id):
    """
    Retrieves a review object:
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    list = []
    for reviw in place.reviews:
        list.append(reviw.to_dict())
    return jsonify(list)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def review_get(review_id):
    """
    Retrieves a place object:
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    """
    Deletes a review object
    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    """
    Creates a Review
    """

    my_place = request.get_json()
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json().keys():
        abort(400, "Missing user_id")
    if "name" not in request.get_json().keys():
        abort(400, "Missing name")
    if "text" not in request.get_json().keys():
        abort(400, "Missing text")
    else:
        my_place['place_id'] = place_id
        revieww = Review(**my_place)
        revieww.save()
        resp = jsonify(revieww.to_dict())
        return (resp), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def review_put(review_id):
    """
    Updates place object
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    my_review = request.get_json()
    if my_review is None:
        abort(400, "Not a JSON")
    else:
        for key, value in my_review.items():
            if key in ['id', 'user_id', 'created_at',
                       'updated_at', 'place_id']:
                pass
            else:
                setattr(review, key, value)
        storage.save()
        resp = review.to_dict()
        return jsonify(resp), 200
