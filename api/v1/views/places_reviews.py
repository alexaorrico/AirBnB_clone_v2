#!/usr/bin/python3
"""
view for reivew objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews')
def get_review_of_places(place_id):
    """Retrieves the list of all places Review objects """
    reviews = storage.all(Review)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    linked_reviews = [
        review.to_dict()
        for review in reviews.values() if review.place_id == place.id
    ]
    return jsonify(linked_reviews)


@app_views.route('/reviews/<review_id>')
def get_review(review_id):
    """"Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a review Object"""
    review = storage.get(Review, review_id)
    all_places = storage.all(Place)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def add_review(place_id):
    """create a review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    if 'user_id' not in request.get_json():
        return ("Missing user_id\n", 400)
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
    if 'text' not in request.get_json():
        return ("Missing text\n", 400)
    request_data = request.get_json()
    request_data['place_id'] = place_id
    request_data['user_id'] = user.id
    new_review = Review(**request_data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """updates a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    request_data = request.get_json()
    request_data.pop('id', None)
    request_data.pop('user_id', None)
    request_data.pop('place_id', None)
    request_data.pop('created_at', None)
    request_data.pop('updated_at', None)
    for key in request_data:
        setattr(review, key, request_data[key])
    review.save()
    return jsonify(review.to_dict()), 200
