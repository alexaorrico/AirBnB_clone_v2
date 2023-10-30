#!/usr/bin/python3
"""states module"""
from api.v1.views import app_views
from flask import jsonify, Flask, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from  models.review import Review


@app_views.route("places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def all_review_by_id(place_id):
    """return json"""
    review_list = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def all_reviews(review_id):
    """return json"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_review_by_id(review_id):
    """return json"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def post_reviews(place_id):
    """return json"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    place = request.get_json()
    user = storage.get(User, place['user_id'])

    if not user:
        abort(404)
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    place["place_id"] = place_id
    ct = Review(**place)
    ct.save()
    return make_response(jsonify(ct.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def put_review_by_id(review_id):
    """return json"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
