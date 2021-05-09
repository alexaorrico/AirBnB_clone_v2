#!/usr/bin/python3

"""
Create a new view for Review objects that handles
all default RestFul API actions.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.review import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Return all objects """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    rList = []
    for r in reviews:
        rList.append(r.to_dict())
    return jsonify(r_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_by_id(review_id):
    """ Retrieve an object """
    obj = storage.get(Review, review_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete an object """
    obj = storage.get(Review, review_id)
    if obj:
        obj.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Create an review """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if not body.get('user_id'):
        abort(400, "Missing user_id")
    user_id = body.get('user_id')
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not body.get('text'):
        abort(400, "Missing text")
    body['place_id'] = place_id
    obj = Review(**body)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Update an object """
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    for k, v in body.items():
        if k not in ['id', 'user_id', 'place_id',
                     'created_at', 'updated_at']:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
