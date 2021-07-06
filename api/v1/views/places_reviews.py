#!/usr/bin/python3
""" View for Review object that handles all default RestFul API actions """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_review(place_id):
    """ Retrieves the list of all Review objects of a Place:
        GET /api/v1/places/<place_id>/reviews
    """
    dict_place = storage.get(Place, place_id)

    if dict_place is None:
        abort(404)

    ret_list = []
    for value in dict_place.reviews:
        ret_list.append(value.to_dict())

    return jsonify(ret_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review_by_id(review_id):
    """ Retrieves a Review object. :
        GET /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object:
        DELETE /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return (jsonify({})), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """ Creates a Review:
        POST /api/v1/places/<place_id>/reviews
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    req_json = request.get_json()
    if not req_json:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'user_id' not in req_json.keys():
        return jsonify({'error': 'Missing user_id'}), 400

    user = storage.get(User, req_json["user_id"])
    if not user:
        abort(404)

    if 'text' not in req_json.keys():
        return jsonify({'error': "Missing text"}), 400

    review = Review(place_id=place_id, **req_json)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """ Updates a Review object:
        PUT /api/v1/reviews/<review_id>
    """
    req_json = request.get_json()
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)
    if not req_json:
        return jsonify({'error': 'Not a JSON'}), 400

    for attr, val in req_json.items():
        setattr(review, attr, val)

    review.save()
    return jsonify(review.to_dict()), 200
