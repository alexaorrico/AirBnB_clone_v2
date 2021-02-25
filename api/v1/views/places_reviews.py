#!/usr/bin/python3
""" Places reviews """
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def review_by_id(place_id):
    """ List al reviws in a place id """
    rev = []
    place = storage.all('Review')
    if place:
        for key, value in place.items():
            if value.to_dict()['place_id'] == place_id:
                rev.append(value.to_dict())
        return jsonify(rev)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def review_object(review_id):
    """ """
    rev = storage.get(Review, review_id)
    if rev:
        return jsonify(rev.to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({}))


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"}), 400)
    kwargs = request.get_json()
    if "user_id" not in kwargs:
        return (jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, kwargs["user_id"])
    if user is None:
        abort(404)
    if "text" not in kwargs:
        return (jsonify({"error": "Missing text"}), 400)
    kwargs['place_id'] = place_id
    review = Review(**kwargs)
    review.save()
    return (jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """ """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return (jsonify({'error': 'Not a JSON'}), 400)
    field_list = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, val in request.get_json().items():
        if key not in field_list:
            setattr(review, key, val)
    storage.save()
    return (jsonify(review.to_dict()), 200)
