#!/usr/bin/python3
"""
Module creates an api view for Review objects
"""

from flask import jsonify, abort, request
from api.v1.views.__init__ import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def place_to_review_index(place_id):
    """
    Retrieves all reviews under place place_id on
    GET /api/v1/places/<place_id>/reviews
    """
    parent_obj = storage.get(Place, place_id)
    if parent_obj is None:
        abort(404)
    else:
        all_reviews_raw = parent_obj.reviews
        all_reviews = []
        for review in all_reviews_raw:
            all_reviews.append(review.to_dict())
        return jsonify(all_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_by_id(review_id):
    """
    Retrieves review object by its id on
    GET /api/v1/reviews/<review_id>
    """
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """
    Deletes a review object on
    DELETE /api/v1/reviews/<review_id> request
    """
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """
    Rereviews a review object on
    PUT /api/v1/reviews/<review_id> request
    """
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)

    else:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            abort(400, description='Not a JSON')
        else:
            json = request.get_json()
            if json is None:
                abort(400, description='Not a JSON')
            for key, value in json.items():
                if key not in [
                    'id', 'user_id', 'place_id', 'created_at', 'updated_at'
                ]:
                    setattr(obj, key, value)
                obj.save()
            return review_by_id(review_id), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """
    Posts a review object and adds it to its parent place
    POST /api/v1/places/<place_id>/reviews request
    """
    parent_obj = storage.get(Place, place_id)
    if parent_obj is None:
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        abort(400, description='Not a JSON')
    else:
        json = request.get_json()
        if json is None:
            abort(400, description='Not a JSON')
        if 'text' not in json.keys():
            abort(400, description='Missing text')
        elif 'user_id' not in json.keys():
            abort(400, description='Missing user_id')

        all_users = list(storage.all(User).values())
        all_user_ids = list(user.id for user in all_users)

        if json['user_id'] not in all_user_ids:
            abort(404)
        else:
            obj = Review(**json)
            obj.place_id = place_id
            obj_id = obj.id
            obj.save()
            return review_by_id(obj_id), 201
