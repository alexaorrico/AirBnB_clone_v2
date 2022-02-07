#!/usr/bin/python3
'''reviews blueprint'''

import re
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def getReviewsInPlace(place_id=None):
    '''get all reviewss in a place'''
    if place_id is None:
        abort(404)
    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)

    reviews = storage.all(Review)
    res = []
    for rev in reviews.values():
        if rev.place_id == pl.id:
            res.append(rev)

    return jsonify([rev.to_dict() for rev in res])


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def getReviewById(review_id=None):
    '''gets review by id'''
    if review_id is None:
        abort(404)
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def deleteReview(review_id=None):
    '''deletes a review'''
    if review_id is not None:
        res = storage.get(Review, review_id)
        if res is not None:
            storage.delete(res)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def postReview(place_id):
    '''posts a new Review'''
    if place_id is None:
        abort(404)
    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in body.keys():
        abort(400, 'Missing user_id')

    user = storage.get(User, body['user_id'])
    if user is None:
        abort(404)
    if 'text' not in body.keys():
        abort(400, 'Missing text')

    body['place_id'] = pl.id
    rev = Review(**body)
    rev.save()
    return make_response(jsonify(rev.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def updateReview(review_id=None):
    '''updates a review'''
    if review_id is None:
        abort(404)
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    for key in body.keys():
        if key not in ['id', 'created_at',
                       'updated_at', 'place_id', 'user_id']:
            setattr(obj, key, body[key])
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
