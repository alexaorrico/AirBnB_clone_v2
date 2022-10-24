#!/usr/bin/python3
""" New view for review object that handles all
default RESTFul API actions. """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_review_id(review_id):
    """ Retrieves, updates or deletes a review object given its id. """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        req_data = request.get_json()
        if not req_data:
            abort(400, description='Not a JSON')

        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

        for key, value in req_data.items():
            if key not in ignore_keys:
                setattr(review, key, value)

        storage.save()
        return make_response(jsonify(review.to_dict()), 200)


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def place_reviews(place_id):
    """ Retrieves all review objects for a place and creates
    a new review object for a place given the place's id.
    Returns 404 error if id is not found.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        list_reviews = [review.to_dict() for review in place.reviews]
        return jsonify(list_reviews)

    if request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            abort(400, description='Not a JSON')

        if "user_id" not in req_data:
            abort(400, description="Missing user_id")

        user = storage.get(User, req_data['user_id'])
        if not user:
            abort(404)

        if "text" not in req_data:
            abort(400, description="Missing text")

        req_data['place_id'] = place_id
        review = Review(**req_data)
        review.save()
        return make_response(jsonify(review.to_dict()), 201)
