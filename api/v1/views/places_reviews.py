#!/usr/bin/python3
"""
Create a new view for Place objects
that handles all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.review import Review
from models import storage
from models.user import User
from flasgger.utils import swag_from


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get.yml', methods=['GET'])
def retrieve_all_reviews(place_id):
    """ Retrieves the list of all Review objects of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review = [review.to_dict() for review in place.review]
    return jsonify(review)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place/get_id.yml', methods=['GET'])
def retrieve_review(review_id):
    """Retrieves a review object by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    dict_review = review.to_dict()
    return jsonify(dict_review)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/review/delete.yml', methods=['DELETE'])
def del_review(review_id):
    """ delete review by place_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/review/post.yml', methods=['POST'])
def create_review(place_id):
    """creates a Review instance"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'text' not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)
    info = request.get_json()
    user = storage.get(User, info['user_id'])
    if not user:
        abort(404)

    info['place_id'] = place_id
    review = Review(**info)
    return (jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/review/put.yml', methods=['PUT'])
def update_review(review_id):
    """updates Place object based on the id"""
    review = storage.get(Review, review_id)
    if review:
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        attr_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in attr_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
