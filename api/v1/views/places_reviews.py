#!/usr/bin/python3
""" Routes places reviews """
from flask import request, abort, jsonify
from api.v1.app import *
from api.v1.views import *
from models import storage, place, user
from models.review import Review


def validate(cls, review_id):
    """ validate if query have id to reference """
    try:
        valid = storage.get(cls, review_id)
        valid.to_dict()
    except Exception:
        abort(404)
    return valid


def get_reviews(place_id, review_id):
    """ get all reviews """
    if (review_id is not None):
        get_review = validate(Review, review_id)
        return jsonify(get_review)
    get_place = storage.get(place.Place, place_id)
    try:
        all_reviews = get_place.reviews
    except Exception:
        abort(404)
    reviews = []
    for review in all_reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


def delete_review(review_id):
    """ delete review on request """
    review = validate(Review, review_id)
    storage.delete(review)
    storage.save()
    response = {}
    return jsonify(response)


def create_review(request, place_id):
    """ create review on place """
    request_json = request.get_json()
    if (request_json is None):
        abort(400, 'Not a JSON')
    try:
        user_id = request_json['user_id']
    except KeyError:
        abort(400, "Missing user_id")
    validate(user.User, user_id)
    try:
        review_text = request_json['text']
    except KeyError:
        abort(400, "Missing text")
    review = Review(text=review_text, place_id=place_id,
                           user_id=user_id)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict())


def update_review(review_id, request):
    """ update review """
    get_review = validate(Review, review_id)
    request_json = request.get_json()
    if (request_json is None):
        abort(400, 'Not a JSON')
    for key, value in request_json.items():
        if (key not in ('id', 'created_at', 'updated_at')):
            setattr(get_review, key, value)
        storage.save()
        return jsonify(get_review.to_dict())


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 defaults={'review_id': None}, strict_slashes=False)
@app_views.route('/reviews/<review_id>', defaults={'review_id': None},
                 methods=['GET', 'DELETE', 'PUT'])
def reviews(place_id, review_id):
    """ Switch to select function """
    if (request.method == "GET"):
        return get_reviews(place_id, review_id)
    elif request.method == "DELETE":
        return delete_review(review_id)
    elif request.method == "POST":
        return create_review(request, place_id), 201
    elif request.method == 'PUT':
        return update_review(review_id, request), 200