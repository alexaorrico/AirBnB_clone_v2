#!/usr/bin/python3
""" Module for Riview objects that handles all default RESTFul API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_all_reviews(place_id):
    """ Retrieves the list of all Rivew objects of a Place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    all_reviews = storage.all(Review).values()
    review_list = []

    for review in all_reviews:
        if place_id == review.to_dict()['place_id']:
            review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a Review object """
    request_data = request.get_json()
    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    if not request_data:
        abort(400, description="Not a JSON")
    if 'user_id' not in request_data:
        abort(400, description="Missing user_id")

    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)

    if 'text' not in request_data:
        abort(400, description="Missing text")

    new_review = Review()
    new_review.place_id = place_id
    new_review.user_id = request_data['user_id']
    new_review.text = request_data['text']

    storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in request_data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
