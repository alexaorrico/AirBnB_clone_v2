#!/usr/bin/python3
'''reviews file'''
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews_place(place_id):
    '''gets reviews of a place'''
    try:
        place = storage.get(Place, place_id)
    except KeyError:
        abort(404)
    if place is None:
        abort(404)
    all_reviews = storage.all(Review)
    reviews_place = []
    for review in all_reviews.values():
        if review.place_id == place.id:
            reviews_place.append(review.to_dict())
    return jsonify(reviews_place)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def req_review(review_id):
    '''gets a specific review'''
    try:
        review = storage.get(Review, review_id)
    except KeyError:
        abort(404)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    '''deletes a specific review'''
    try:
        review = storage.get(Review, review_id)
    except KeyError:
        abort(404)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    '''creates a review'''
    try:
        place = storage.get(Place, place_id)
    except KeyError:
        abort(404)
    if place is None:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    user_id = data.get('user_id')
    if user_id is None:
        abort(400, 'Missing user_id')
    try:
        user = storage.get(User, user_id)
    except KeyError:
        abort(404)
    if user is None:
        abort(404)
    text = data.get('text')
    if text is None:
        abort(400, 'Missing text')
    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''updates a specific review'''
    try:
        review = storage.get(Review, review_id)
    except KeyError:
        abort(404)
    if review is None:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
