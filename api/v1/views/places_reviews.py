#!/usr/bin/python3
"""
contains endpoints(routes) for review objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<string:place_id>/reviews", strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all review objects of a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [obj.to_dict() for obj in places.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<string:review_id>", strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<string:review_id>", strict_slashes=False,
                 methods=['DELETE'])
def del_review(review_id):
    """
    Deletes a review object
    """
    review = storage.get(Review, review_id)
    if review:
        review.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/places/<string:place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """
    Creates a review instance
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    valid_json = request.get_json()

    if valid_json is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in valid_json:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'text' not in valid_json:
        return make_response(jsonify({"error": "Missing text"}), 400)

    valid_json['place_id'] = place_id
    user = storage.get(User, valid_json['user_id'])
    if not user:
        abort(404)
    obj = Review(**valid_json)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/reviews/<string:review_id>", strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """
    Updates a review object
    """
    review = storage.get(Review, review_id)
    valid_json = request.get_json()

    if not review:
        abort(404)

    if valid_json is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in valid_json.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
