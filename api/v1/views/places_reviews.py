#!/usr/bin/python3
"""Handles the user view
"""

# from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_revs(place_id):
    """Gets the dict containing all reviews of a places
    """
    place = storage.get("Place", place_id)
    if place is None:
        return abort(404)
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_revs_id(review_id):
    """Gets a review by its ID
    """
    review = storage.get("Review", review_id)
    if review is not None:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review
    """
    review = storage.get("Review", review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a review
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    got_json = request.get_json()
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in got_json:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    a_user = storage.get("User", got_json['user_id'])
    if a_user is None:
        abort(404)
    if 'text' not in got_json:
        return make_response(jsonify({"error": "Missing text"}), 400)
    new_rev = Review(**got_json)
    storage.new(new_rev)
    new_rev.place_id = place.id
    storage.save()
    return make_response(jsonify(new_rev.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_rev(review_id):
    """Updates a review
    """
    got_json = request.get_json()
    list_ign = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    rev = storage.get("Review", review_id)
    if rev:
        for key, val in got_json.items():
            setattr(rev, key, val)
        storage.save()
        return make_response(jsonify(rev.to_dict()), 200)
    else:
        abort(404)
