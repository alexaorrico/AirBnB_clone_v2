#!/usr/bin/python3
"""Review module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flasgger.utils import swag_from


# GET
@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/reviews/get.yml', methods=['GET'])
def get_reviews(place_id):
    """Retrieve Review objects"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    reviews = [obj.to_dict() for obj in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_id.yml', methods=['GET'])
def get_review(review_id):
    """Retrieve Review object by id"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


# DELETE
@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/reviews/delete.yml', methods=['DELETE'])
def delete_review(review_id):
    """Delete Review object"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({})


# POST
@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/reviews/post.yml', methods=['POST'])
def create_review(place_id):
    """Creates Review object"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    if 'text' not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)

    kwargs = request.get_json()
    kwargs['place_id'] = place_id
    user = storage.get(User, kwargs['user_id'])

    if user is None:
        abort(404)

    obj = Review(**kwargs)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


# PUT
@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/reviews/put.yml', methods=['PUT'])
def update_review(review_id):
    """Updates Review object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(Review, review_id)

    if obj is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated']:
            setattr(obj, key, value)

    storage.save()
    return jsonify(obj.to_dict())
