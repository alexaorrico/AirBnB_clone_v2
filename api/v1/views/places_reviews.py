#!/usr/bin/python3
"""
module to generate json response
"""

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def all_reviews(place_id):
    """ display all reviews """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    response = []
    reviews = place.reviews
    for review in reviews:
        response.append(review.to_dict())
    return jsonify(response)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def review_by_id(place_id=None):
    """ display review by id """
    response = storage.get(Review, review_id)
    if response is None:
        abort(404)
    return jsonify(response.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id=None):
    """ delete review by id """
    if review_id is None:
        abort(404)
    else:
        trash = storage.get(Review, review_id)
        if trash is not None:
            storage.delete(trash)
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ create new review to a specific place """
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    body = request.get_json()
    if body is None or type(body) is not dict:
        abort(400, 'Not a JSON')
    if 'text' not in body.keys():
        abort(400, 'Missing text')
    if 'user_id' not in body.keys():
        abort(400, 'Missing user_id')
    if storage.get(User, body['user_id']) is None:
        abort(400)
    body['place_id'] = place_id
    obj = Review(**body)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id=None):
    """ update an existing review """
    response = storage.get(Review, review_id)
    if review_id is None or response is None:
        abort(404)
    try:
        new = request.get_json()
    except Exception:
        pass
    if new is None or type(new) is not dict:
        abort(400, 'Not a JSON')
    for key in new.keys():
        if key != 'id' and key != 'created_at' and key != 'place_id' and\
           key != 'user_id' and key != 'updated_at':
            setattr(response, key, new[key])
    response.save()
    return make_response(jsonify(response.to_dict()), 200)
