#!/usr/bin/python3
"""API endpoints for reviews"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.review import Review


def get_obj_or_abort(obj_cls, obj_id):
    """Retrieve an object by ID or abort with 404 if not found"""
    obj = storage.get(obj_cls, obj_id)
    if obj is None:
        abort(404)
    return obj


def create_review(data, place_id):
    """Create a new city in the database."""
    data['place_id'] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return new_review


def validate_json():
    """Validate that the request data is in JSON format."""
    try:
        return request.get_json()
    except Exception:
        abort(400, "Not a JSON")


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET', 'POST'])
def cities_by_state(place_id=None):
    """Route for retrieving Review objects"""

    if request.method == 'GET':
        # Get a list of all Review object for a place
        place = get_obj_or_abort('Place', place_id)
        reviews_list = [review.to_dict() for review in place.reviews]
        return jsonify(reviews_list)

    if request.method == 'POST':
        # Add a State to the list
        get_obj_or_abort('Place', place_id)
        data = validate_json()
        if "user_id" not in data:
            abort(400, "Missing user_id")
        get_obj_or_abort('User', data['user_id'])
        if "text" not in data:
            abort(400, "Missing text")
        new_review = create_review(data, place_id)
        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def city_with_id(review_id=None):
    """Route for manipulating a specific City object"""

    review = get_obj_or_abort('Review', review_id)

    if request.method == 'GET':
        # Get a specific state by id
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        # Delete a specific state by id
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        # Update a specific state by id
        data = validate_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at",
                           "place_id", "user_id"]:
                setattr(review, key, value)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
