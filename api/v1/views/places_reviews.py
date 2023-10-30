#!/usr/bin/python3
"""Module containing a Flask Blueprint routes that handles
all default RESTFul API actions for Review resource"""
from api.v1.views import app_views
from flask import abort, make_response, jsonify, request
from markupsafe import escape
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


def retrive_object(cls, id):
    """Retrives a resource based on given class and id."""
    obj = storage.get(cls, escape(id))
    if obj is None:
        abort(404)
    return (obj)


def validate_request_json(request):
    """Checks validity of request's json content"""
    if not request.is_json:
        abort(make_response(jsonify(error="Not a JSON"), 400))
    req_json = request.get_json()
    if request.method == 'POST':
        if 'user_id' not in req_json:
            abort(make_response(jsonify(error="Missing user_id"), 400))
        retrive_object(User, req_json['user_id'])
        if 'text' not in req_json:
            abort(make_response(jsonify(error="Missing text"), 400))
    return (req_json)


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def places_reviews_get(place_id):
    """Returns a list of reviews for a Place resource with given id"""
    obj = retrive_object(Place, place_id)
    reviews = [review.to_dict() for review in obj.reviews]
    return (jsonify(reviews))


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def reviews_get(review_id):
    """Returns a Review resource based on given id"""
    obj = retrive_object(Review, review_id)
    return (jsonify(obj.to_dict()))


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def reviews_delete(review_id):
    """Deletes a Review resource based on given id"""
    obj = retrive_object(Review, review_id)
    storage.delete(obj)
    storage.save()
    return (jsonify({}))


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def places_reviews_post(place_id):
    """Creates a Review resource for a Place of given id
    if request content is valid."""
    obj = retrive_object(Place, place_id)
    req_json = validate_request_json(request)
    req_json['place_id'] = obj.id
    new_review = Review(**req_json)
    new_review.save()
    return (jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def reviews_put(review_id):
    """Updates a Review resource of given id if request content is valid."""
    obj = retrive_object(Review, review_id)
    req_json = validate_request_json(request)
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore:
            setattr(obj, key, value)
    obj.save()
    return (jsonify(obj.to_dict()))
