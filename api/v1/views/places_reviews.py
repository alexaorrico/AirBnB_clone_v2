#!/usr/bin/python3
""" view for place """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def retrieve_reviews(place_id):
    """ function to retrieve related reviews """
    if place_id is None:
        return abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    reviews = place.reviews
    list_reviews = []
    for review in reviews:
        list_reviews.append(review.to_dict())
    return jsonify(list_reviews)


@app_views.route('reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_reviews(review_id):
    """ retrieves place by id """
    if review_id is None:
        return abort(404)
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ function to delete place instance """
    if review_id is None:
        return abort(404)
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ post a new place """
    if place_id is None:
        return abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if not request.json:
        return 'Not a JSON', 400
    if 'user_id' not in request.json:
        return 'Missing user_id', 400
    user = storage.get(User, request.json.get('user_id'))
    if user is None:
        return abort(404)
    if 'text' not in request.json:
        return 'Missing text', 400

    data = request.get_json()
    review = Review(**data)
    review.place_id = place.id
    review.save()
    review_dict = review.to_dict()
    return jsonify(review_dict), 201


@app_views.route('reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ update place instance """
    if review_id is None:
        return abort(404)
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    if not request.json:
        return 'Not a JSON', 400
    body = request.get_json()
    for key, value in body.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at' or\
                key == 'user_id' or key == 'place_id':
            continue
        setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
