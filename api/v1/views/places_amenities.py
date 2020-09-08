#!/usr/bin/python3
""" amenities view class """
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from flask import jsonify, request, abort, make_response
import os


@app_views.route("/places/<string:place_id>/amenities",
                 strict_slashes=False, methods=["GET"])
def get_amenities_from_place(place_id=None):
    """ retrives all amenities from a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        return jsonify([amenity.to_dict() for amenity in place.amenity_ids])


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 strict_slashes=False, methods=["DELETE", "POST"])
def dev_get_amenity_id(review_id=None):
    """ gets amenity by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == "DELETE":
        review.delete()
        storage.save()
        return jsonify({})
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

        return jsonify(review.to_dict())
