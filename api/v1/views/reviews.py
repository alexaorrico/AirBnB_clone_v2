#!/usr/bin/python3
"""View for Reviews"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.place import Place
from models.review import Review
from models.user import User
from flask import abort
from flask import make_response
from flask import request


@app_views.route('places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_reviews(place_id):
    """Return reviews according to id of place object
        or return error: Not found if it doesn't exist.
    """
    if place_id:
        dict_place = storage.get(Place, place_id)
        if dict_place is None:
            abort(404)
        else:
            reviews = storage.all(Review).values()
            list_reviews = []
            for review in reviews:
                if review.place_id == place_id:
                    list_reviews.append(review.to_dict())
            return jsonify(list_reviews)


@app_views.route('reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """Return review object according class and id of the review
        or return Error: Not found if it doesn't exist.
    """
    if review_id:
        dict_review = storage.get(Review, review_id)
        if dict_review is None:
            abort(404)
        else:
            return jsonify(dict_review.to_dict())


@app_views.route('reviews/<review_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Deletes an object Review if exists, otherwise raise
        404 error
    """
    if review_id:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        else:
            storage.delete(review)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def response_reviews(place_id):
    """Post request that allow to create a new review if exists the name
        or raise Error if is not a valid json or if the name is missing
    """
    if place_id:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()

    if "user_id" not in req:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)

    if "text" not in req:
        return make_response(jsonify({"error": "Missing text"}), 400)
    req['place_id'] = place_id
    reviews = Review(**req)
    reviews.save()
    return make_response(jsonify(reviews.to_dict()), 201)


@app_views.route('reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """Updates attributes from an review object"""
    if review_id:
        obj_reviews = storage.get(Review, review_id)
        if obj_reviews is None:
            abort(404)
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in [
                'id',
                'user_id',
                'place_id',
                'created_at',
                    'updated_at']:
                setattr(obj_reviews, key, value)
        obj_reviews.save()
        return make_response(jsonify(obj_reviews.to_dict()), 200)
