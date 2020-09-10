#!/usr/bin/python3
""" Places """

from flask import jsonify, request, abort
from flask import make_response
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=["GET", "POST"],
                 strict_slashes=False)
def reviews_place(place_id):
    """ Retrieves the list of all Places objects """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        review = storage.all(Review).values()
        all_review = []
        for key in review.values():
            if key.place_id == place_id:
                all_review.append(key.to_dict())
        return jsonify(all_review)
    if request.method == "POST":
        response = request.get_json()
        if response is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "user_id" not in response:
            return make_response(jsonify({"error": "Missing user_id"}), 400)
        if user is None:
            abort(404)
        if "text" not in response:
            return make_response(jsonify({"error": "Missing text"}), 400)
        response['place_id'] = place_id
        new_review = Review(**response)
        new_review.save()
        return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def place_review(review_id):
    """ Manipulate an specific Place """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    if request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    if request.method == "PUT":
        response = request.get_json()
        if response is None:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        for key, value in response.items():
            if key not in ["id", "user_id", "place_id", "created_at",
                           "updated_at"]:
                setattr(review, key, value)
        review.save()
        return make_response(jsonify(review.to_dict()), 200)
