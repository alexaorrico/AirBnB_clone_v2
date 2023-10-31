#!/usr/bin/python3
''' comment '''

from flask import Blueprint, abort, jsonify, request
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User


places_reviews = Blueprint('places_reviews', __name__)


@places_reviews.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def handle_place_reviews(place_id):
    # Check if the place_id is linked to a Place object
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        # Retrieve the list of all Review objects of a Place
        reviews = storage.all(Review).values()
        get_all = []
        for rev in reviews:
            if rev.place_id == place_id:
                get_all.append(rev.to_dict())
        return jsonify(get_all)

    elif request.method == 'POST':
        # Create a new Review
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        data = request.get_json()
        if "user_id" not in data:
            return make_response(jsonify({"error": "Missing user_id"}), 400)
        user = storage.get(User, data["user_id"])
        if user is None:
            abort(404)
        if "text" not in data:
            return make_response(jsonify({"error": "Missing text"}), 400)
        data["place_id"] = place_id
        new = Review(**data)
        new.saave()
        return make_response(jsonify(new.to_dict()), 201)


@places_reviews.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_review(review_id):
    # Retrieve the Review object
    review = Review.get(review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        # Retrieve a Review object
        return jsonify(review.to_dict())

    elif request.method == 'DELETE':
        # Delete a Review object
        review.delete()
        review.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        # Update a Review object
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

    # Ignore keys: id, user_id, place_id, created_at, and updated_at
    ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(review, key, value)

    review.save()
    return make_response(jsonify(review.to_dict()), 200)
