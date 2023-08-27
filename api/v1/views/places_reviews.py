#!/usr/bin/python3
""" View for Reviews """

from flask import jsonify, abort, request, make_response
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from models import storage
from sqlalchemy.exc import IntegrityError


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """ Retrieves the list of all Review objects for a specific Place """
    places_dict = storage.all(Place)
    reviews_list = None
    return_list = []
    for place in places_dict.values():
        if place.id == place_id:
            reviews_list = place.reviews
    if reviews_list is None:
        abort(404)
    for review in reviews_list:
        return_list.append(review.to_dict())
    return jsonify(return_list)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Retrieves a specific Review object by its ID """
    review = storage.get(Review, review_id)
    if review is not None:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a specific Review object by its ID """
    review = storage.get(Review, review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a new Review object for a specific Place """
    try:
        request_dict = request.get_json(silent=True)
        if request_dict is not None:
            if 'user_id' not in request_dict.keys():
                return make_response(
                    jsonify({"error": "Missing user_id"}), 400)
            if 'text' in request_dict.keys():
                request_dict['place_id'] = place_id
                new_review = Review(**request_dict)
                new_review.save()
                return make_response(jsonify(new_review.to_dict()), 201)
            return make_response(jsonify({'error': 'Missing text'}), 400)
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    except IntegrityError:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a specific Review object by its ID """
    request_dict = request.get_json(silent=True)
    if request_dict is not None:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        for key, val in request_dict.items():
            if key not in ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']:
                setattr(review, key, val)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)
