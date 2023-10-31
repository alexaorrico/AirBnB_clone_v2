#!/usr/bin/python3
"""Flask route for review model"""

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.review import Review
from models.place import Place
from os import environ
STOR_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews(place_id=None):
    """route to return all reviews"""

    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404, 'Not found')

    if request.method == "GET":
        reviews_dict = storage.all(Review)
        reviews_list = [obj.to_dict()
                        for obj in reviews_dict.values()
                        if obj.place_id == place_id
                        ]
        return jsonify(reviews_list)

    if request.method == "POST":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        if request_json.get("user_id") is None:
            abort(400, "Missing user_id")
        if storage.get("User", request_json.get("user_id")) is None:
            abort(404, "Not found")
        if request_json.get("name") is None:
            abort(400, "Missing name")

        request_json["place_id"] = place_id
        newReview = Review(**request_json)
        newReview.save()
        return make_response(jsonify(newReview.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"])
def review(review_id=None):
    """Get, update or delete review with review id"""
    review_obj = storage.get(Review, review_id)

    if review_obj is None:
        abort(404, "Not found")

    if request.method == "GET":
        return jsonify(review_obj.to_dict())

    if request.method == "DELETE":
        review_obj.delete()
        storage.save()
        return jsonify({})

    if request.method == "PUT":
        request_json = request.get_json()
        if request_json is None:
            abort(400, "Not a JSON")
        review_obj.update(request_json)
        return make_response(jsonify(review_obj.to_dict()), 200)
