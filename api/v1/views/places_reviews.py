#!/usr/bin/python3
"""
places
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id):
    """ Get All Reviews of Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_review(review_id):
    """Get Review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """ DELETE user With id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()

    return jsonify({}), 200


