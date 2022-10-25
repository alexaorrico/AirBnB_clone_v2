#!/usr/bin/python3
""" Flask views for the Places resource """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_reviews(place_id):
    """ An endpoint that returns all reviews """
    rlist = []
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    for review in reviews:
        rlist.append(review.to_dict())
    return jsonify(rlist)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """ An endpoint that returns a specific review """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    else:
        return(jsonify(review.to_dict()))


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """ An endpoint that deletes a specific review """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """ An endpoint that creates a new review """
    req_fields = ['user_id', 'text']
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    for field in req_fields:
        if field not in content:
            abort(400, 'Missing {}'.format(field))
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    user = storage.get('User', content['user_id'])
    if user is None:
        abort(404)
    content['place_id'] = place_id
    review = Review(**content)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def modify_review(review_id):
    """ An endpoint that modifies an existing review """
    ignored_keys = ['id', 'user_id', 'place_id', 'created_at',
                    'updated_at']
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    for k, v in content.items():
        if k not in ignored_keys:
            setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 200
