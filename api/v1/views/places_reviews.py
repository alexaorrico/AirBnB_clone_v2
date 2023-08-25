#!/usr/bin/python3
"""
    This module creates a new view for Review
    objects that handles all default REST API
    actions.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET'], strict_slashes=False)
def get_reviews_of_place(place_id):
    """Get the reviews linked to a place object"""
    place = storage.get(Place, place_id)
    if place:
        reviews = place.reviews
        review_list = []
        for review in reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>",
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Get a specific review from the db"""
    search_result = storage.get(Review, review_id)
    if search_result:
        return jsonify(search_result.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a specific review from the db"""
    search_result = storage.get(Review, review_id)
    if search_result:
        storage.delete(search_result)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def post_new_review(place_id):
    """Post a new review to the db"""
    place = storage.get(Place, place_id)
    if place:
        try:
            rev_dict = request.get_json()
            rev_dict.update({"place_id": place_id})

        except Exception:
            return jsonify({"error": "Not a JSON"}), 400

        u_id = rev_dict.get("user_id")
        if u_id:
            usr = storage.get(User, u_id)
            if usr:
                if rev_dict.get("text"):
                    new_review = Review(**rev_dict)
                    storage.new(new_review)
                    storage.save()
                    return jsonify(new_review.to_dict()), 201
                else:
                    return jsonify({"error": "Missing text"}), 400
            else:
                abort(404)
        return jsonify({"error": "Missing user_id"}), 400

    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def modify_review(review_id):
    """Modify an existing review in the db"""
    review = storage.get(Review, review_id)
    if review:
        try:
            update_dict = request.get_json()
            for key in ('id', 'created_at', 'updated_at'):
                if update_dict.get(key):
                    del update_dict[key]

        except Exception:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in update_dict.items():
            setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200

    else:
        abort(404)
