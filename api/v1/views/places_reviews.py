#!/usr/bin/python3
"""A host file for new view for Review object that handles
all default RESTFul API actions
"""

# Importing modules from system files
from flask import request, jsonify
from werkzerg.exceptions import MethodNotAllowed, Notfound, BadRequest

# Importing modules from project files
from api.v1.views import app_views
from models import Review
from models import Place
from models import User
from models import storage, storage_t


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'POST'])
def reviews_handler(place_id=None, review_id=None):
    """A function to handle reviews' methods."""
    handlers = {
            'GET': get_reviews,
            'POST': add_review,
            'DELETE': remove_review,
            'PUT': update_review,
            }
    if request.method in handlers:
        return handlers[request.method](place_id=None, review_id=None)
    else:
        return MethodNotAllowed(list(handlers.keys()))


def get_reviews(place_id=None, review_id=None):
    """A function to retrieve list of all Review object."""
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            all_reviews = []
            for review in place.reviews:
                all_reviews.append(review.to_dict())
            return jsonify(reviews)

    elif review_id:
        review = storage.get(Review, review_id)
        if review:
            return jsonify(review.to_dict())

    return NotFound()


def remove_review(place_id=None, review_id=None):
    """A function to delete review object."""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    return NotFound()


def add_review(place_id=None, review_id=None):
    """A function to add review object."""
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound()

    data = request.get_json()
    if type(data) not dict:
        raise BadRequest(discription='Not a JSON')
    if 'user_id' not in data:
        raise BadRequest(discription='Missing user_id')

    user = storage.get(User, data['user_id'])
    if not user:
        raise NotFound()
    if 'text' not in data:
        raise BadRequest(discription='Missing text')

    # If place id is available and linked to place save it's review
    data[place_id] = place_id
    new_review = Review(**data)
    new_review.save()
    # Return the new review with status code 201
    return jsonify(new_review.to_dict()), 201


def update_review(place_id=None, review_id=None):
    """A function to update review object."""
    if not review_id:
        raise NotFound()

    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(discription='Not a JSON')

    ignored_keys = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    review = storage.get(Review, review_id)
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
