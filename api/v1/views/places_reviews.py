#!/usr/bin/python3
""" amenities view class """
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from flask import jsonify, request, abort, make_response


@app_views.route("/places/<string:place_id>/reviews",
                 strict_slashes=False, methods=["GET", "POST"])
def get_review_from_place(place_id=None):
    """ retrives all reviews from a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify([review.to_dict() for review in place.reviews])
    if request.method == "POST":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if request.get_json().get("user_id") is None:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        if request.get_json().get("text") is None:
            return make_response(jsonify({'error': 'Missing text'}), 400)
        user = storage.get(User, request.get_json().get("user_id"))
        if user is None:
            abort(404)
        dic = request.get_json()
        dic.update({"place_id": place_id})
        review = Review(**dic)
        review.save()
        return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<string:review_id>",
                 strict_slashes=False, methods=["GET", "DELETE", "PUT"])
def get_review_id(review_id=None):
    """ gets review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    if request.method == "DELETE":
        review.delete()
        storage.save()
        return jsonify({})
    if request.method == "PUT":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, val in request.get_json().items():
            if key not in ['id', 'created_at',
                           'updated_at', 'user_id', 'city_id']:
                setattr(review, key, val)
        review.save()
        return jsonify(review.to_dict())
