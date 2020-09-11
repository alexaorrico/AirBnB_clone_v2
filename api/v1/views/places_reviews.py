#!/usr/bin/python3
"""Create a new view for Review objects"""

from flask import jsonify, request, abort
from models.state import State
from models.review import Review
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=["GET", "POST"],
                 strict_slashes=False)
def list_reviews(place_id):
    """ Retrieves the list of all Review objects """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        reviews = storage.all("Review")
        all_review = []
        for key in reviews.values():
            if key.place_id == place_id:
                all_review.append(key.to_dict())
        return jsonify(all_review)
    if request.method == "POST":
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        if "user_id" not in response:
            abort(400, "Missing user_id")
        user = storage.get("User", response["user_id"])
        if user is None:
            abort(404)
        if "text" not in response:
            abort(400, "Missing text")
        response["place_id"] = place_id
        new_review = Review(**response)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def review(review_id):
    """ Manipulate an specific Review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    if request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at', 'user_id',
                           'place_id']:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
