#!/usr/bin/python3
'''This module Retrieves the list of all review objects,
deletes, updates, creates and gets information of a review '''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models import storage


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_all_review(place_id):
    ''' retreive all review associated with the place id '''
    place_objs = storage.all('Place')
    key = 'Place.{}'.format(place_id)

    if key in place_objs:
        place = place_objs.get(key)
        return jsonify([obj.to_dict() for obj in place.reviews])

    abort(404)


@app_views.route('/reviews/<review_id>/', strict_slashes=False)
def get_a_review(review_id):
    '''return the review with matching id'''
    review_objs = storage.all('Review')
    key = 'Review.{}'.format(review_id)

    if key in review_objs:
        review = review_objs.get(key)
        return jsonify(review.to_dict())

    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    ''' delete review matching the id'''
    review_objs = storage.all('Review')
    key = 'Review.{}'.format(review_id)

    if key in review_objs:
        obj = review_objs.get(key)
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/places/<place_id>/reviews/', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    ''' create a review '''

    data = request.get_json()
    place_objs = storage.all('Place')
    key = 'Place.{}'.format(place_id)

    if key not in place_objs:
        abort(404)
    if data is None:  # not a json
        abort(400, "Not a JSON--")
    if data.get('user_id') is None:
        abort(400, "Missing user_id")

    user_objs = storage.all('User')
    user_id = data.get('user_id')
    if 'User.{}'.format(user_id) not in user_objs:
        abort(404)
    if data.get('text') is None:
        abort(400, "Missing text")

    data['place_id'] = place_id
    review_obj = Review(**data)
    review_obj.save()
    return jsonify(review_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    ''' update review  whose id is passed'''
    data = request.get_json()
    review_objs = storage.all('Review')
    key = 'Review.{}'.format(review_id)

    if key not in review_objs:
        abort(404)
    if data is None:
        abort(400, "Not a JSON")

    review = review_objs.get(key)
    for k, v in data.items():
        setattr(review, k, v)
    review.save()

    return jsonify(review.to_dict()), 200
