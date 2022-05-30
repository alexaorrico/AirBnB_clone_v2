#!/usr/bin/python3
""" Review view """
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def list_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review(review_id):
    """ Retrieves a Review object """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    """ Deletes a Review object """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def new_review(place_id):
    """ Creates a new Review """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    new_review = request.get_json()
    if not new_review:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_review:
        abort(400, 'Missing user_id')
    if not storage.get('User', new_review['user_id']):
        abort(404)
    if 'text' not in new_review:
        abort(400, 'Missing text')
    new_review['place_id'] = place_id
    review = Review(**new_review)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_id_put(review_id):
    """ Updates a Review object """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    request_json = request.get_json()
    if not request_json:
        abort(400, 'Not a JSON')
    for key, value in request_json.items():
        if key != 'id' and key != 'user_id' and key != 'place_id' \
                and key != 'created_at' and key != 'updated_at':
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
