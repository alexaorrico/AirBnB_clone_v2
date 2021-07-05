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
    """Return reviews for place id or return error message
    """
    if place_id:
        dict_pl = storage.get(Place, place_id)
        if dict_pl is None:
            abort(404)
        else:
            reviews = storage.all(Review).values()
            list_rev = []
            for review in reviews:
                if review.place_id == place_id:
                    list_rev.append(review.to_dict())
            return jsonify(list_rev)


@app_views.route('reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """Return review for according class and review id or return error message
    """
    if review_id:
        dict_rev = storage.get(Review, review_id)
        if dict_rev is None:
            abort(404)
        else:
            return jsonify(dict_rev.to_dict())


@app_views.route('reviews/<review_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Deletes one Review if exists or raise 404 error
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
    """Create a new review if exists the name or raise Error
        if is not a valid json or if the name is missing
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
        obj_rev = storage.get(Review, review_id)
        if obj_rev is None:
            abort(404)
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        attr = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for k, v in req.items():
            if k not in attr:
                setattr(obj_rev, k, v)
        obj_rev.save()
        return make_response(jsonify(obj_rev.to_dict()), 200)
