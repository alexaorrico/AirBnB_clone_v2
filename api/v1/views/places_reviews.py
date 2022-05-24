#!/usr/bin/python3
""" Reviews """
import json
from models import storage
from flask import jsonify, abort, request, make_response
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=['GET', 'POST'],
                 strict_slashes=False)
def reviews(place_id):
    """ DO some method on Place with a place_id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        list_reviews = []
        for review in place.reviews:
            list_places.append(review.to_dict())
        return jsonify(list_reviews)

    if request.method == 'POST':
        list_user_id = []
        users = storage.all(User).values()
        for user in users:
            list_user_id.append(user.id)
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        if response.get("user_id") is None:
            abort(400, "Missing user_id")
        if response.get("user_id") not in list_user_id:
            abort(404)
        if response.get("text") is None:
            abort(400, "Missing text")

        new = Review(**response)
        new.place_id = place.id
        new.save()
        return make_response(jsonify(new.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review_id(review_id):
    """ Do different methods on a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({})

    elif request.method == 'PUT':
        ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        for key, value in response.items():
            if key not in ignore:
                setattr(review, key, value)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
