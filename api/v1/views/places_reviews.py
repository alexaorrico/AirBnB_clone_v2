#!/usr/bin/python3
"""objects that handle all default RestFul API actions for Places_review """
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentatio/reviews/get.yml', methods=['GET'])
def get_all_review(place_id):
    """get reviews from a specific place"""
    place = storage.get(Place, place_id)

    if not place or if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews)


@app_views.route('/reviews/<review_id', methods=['GET']
                 strict_slashes=False)
@swag_from('documentatio/reviews/get_id.yml', methods=['GET'])
def get_a_review(review_id):
    """Get a review id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id', methods=['DELETE']
                 strict_slashes=False)
@swag_from('documentatio/reviews/get_id.yml', methods=['DELETE'])
def del_a_review(review_id):
    """ Delete a review by review_id"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST']
                 strict_slashes=False)
@swag_from('documentatio/reviews/post.yml', methods=['POST'])
def create_review(place_id):
    """ Create a review using the place_id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify("error": "Missing user_id"), 400)
    if storage.get("User".request.get_json()["user_id"]) is None:
        abort(404)
    if "text" not in request.get_json():
        return jsonify({"error": "Missing text"}), 400
    else:
        data_obj = request.get_json()
        data = Review(**data_obj)
        data.place_id = place_id
        data.save()
        return jsonify(data.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update the review object using PUT method """
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)

    ignore_keys = ("id", "user_id", "place_id", "created_at", "updated_at")
    for key, value in data.items():
        if key in ignore_keys:
            pass
        else:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
