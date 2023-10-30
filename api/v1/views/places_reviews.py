#!/usr/bin/python3
""""
API Review View Module

Defines the API views for the Review objects, providing RESTful
endpoints to interact with Review resources.

HTTP status codes:
- 200: OK: The request has been successfully processed.
- 201: 201 Created: The new resource has been created.
- 400: Bad Request: The server cannot process the request.
- 404: Not Found: The requested resource could not be found on the server.
"""
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    ''' Get all the Review objects linked to a given Place object '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews_list = []
    for elem in place.reviews:
        reviews_list.append(elem.to_dict())
    return jsonify(reviews_list)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    ''' Create a new Review object and link it to the given Place object '''
    if not storage.get(Place, place_id):
        abort(404)
    query = request.get_json()
    if not query:
        abort(400, description='Not a JSON')
    if 'user_id' not in query:
        abort(400, description='Missing user_id')
    if not storage.get(User, query['user_id']):
        abort(404)
    if 'text' not in query:
        abort(400, description='Missing text')
    query['place_id'] = place_id
    new = Review(**query)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    ''' Get a Review object by ID '''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    ''' Delete a Review object '''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    return make_response(jsonify({}), 200)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    ''' Update the values of a given Review object '''
    if not storage.get(Review, review_id):
        abort(404)
    if request.content_type != 'application/json':
        abort(400, description='Not a JSON')
    review = storage.get(Review, review_id)
    query = request.get_json()
    ignore_list = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, val in query.items():
        if key not in ignore_list:
            setattr(review, key, val)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
