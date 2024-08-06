#!/usr/bin/python3
"""Reviews web route """
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_reviews.yml', methods=['GET'])
def get_reviews(place_id):
    """
    retrieve a place reviews
    """
    place_r = storage.get(Place, place_id)

    if not place_r:
        abort(404)

    reviews_p_d = [review.to_dict() for review in place_r.reviews]

    return jsonify(reviews_p_d)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/reviews/get_review.yml', methods=['GET'])
def get_review(review_id):
    """
    retrieves a Review obj
    """
    review_p = storage.get(Review, review_id)
    if not review_p:
        abort(404)

    return jsonify(review_p.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/reviews/delete_reviews.yml', methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a Review Obj
    """

    review_p_ = storage.get(Review, review_id)

    if not review_p_:
        abort(404)

    storage.delete(review_p_)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/reviews/post_reviews.yml', methods=['POST'])
def post_review(place_id):
    """
    Creates a Review a place
    """
    place_np = storage.get(Place, place_id)

    if not place_np:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data_p = request.get_json()
    user_p = storage.get(User, data_p['user_id'])

    if not user_p:
        abort(404)

    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    data_p['place_id'] = place_id
    inst = Review(**data_p)
    inst.save()
    return make_response(jsonify(inst.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/reviews/put_reviews.yml', methods=['PUT'])
def put_review(review_id):
    """
    Updates a Review a placwe
    """
    review_p = storage.get(Review, review_id)

    if not review_p:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore_key = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    data_k = request.get_json()
    for key, value in data_k.items():
        if key not in ignore_key:
            setattr(review_p, key, value)
    storage.save()
    return make_response(jsonify(review_p.to_dict()), 200)
