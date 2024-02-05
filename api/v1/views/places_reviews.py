#!/usr/bin/python3
"""view for review object that handles all default RESTFul API actions"""
from . import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_review_place(place_id):
    """Returns a list of all review objects of a place"""
    place = storage.get(Place, place_id)
    if place:
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Return a dict representation of review object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict()), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review object"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify("{}"), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.json
    if data:
        if 'user_id' not in data:
            return jsonify({"error": "Missing user_id"}), 400
        if 'text' not in data:
            return jsonify({"error": "Missing text"}), 400
        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)
        data['place_id'] = place_id
        review = Review(**data)
        review.save()
        return review.to_dict(), 201
    else:
        return jsonify({"error": "Not a JSON"}), 400


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """updates review object"""
    review = storage.get(Review, review_id)
    skip_list = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    if review:
        if request.json:
            for key, value in request.json.items():
                if key not in skip_list:
                    setattr(review, key, value)
            review.save()
            return review.to_dict(), 200
        else:
            return jsonify({"error": "Not a JSON"}), 400
    else:
        abort(404)
