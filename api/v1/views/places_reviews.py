#!/usr/bin/python3
"""palce"""

from crypt import methods
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models import storage
from sqlalchemy.exc import IntegrityError


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_places(place_id=None):
    """retrieves the list of all City objects"""
    all_places = []
    ob_place = storage.get("place", place_id)
    if ob_place:
        for place_obj in ob_place.places:
            all_places.append(place_obj.to_dict())
        return jsonify(all_places)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_place(review_id=None):
    """retrieves a Place object"""
    review_id = storage.get("Review", review_id)
    if review_id:
        return jsonify(review_id.to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """deletes a Place object"""
    review_obj = storage.get("Review", review_id)
    if review_obj:
        storage.delete(review_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_place(place_id):
    """creates a city object"""
    place_obj = storage.get("Place", place_id)
    obj_request = request.get_json()
    try:
        if place_obj:
            if obj_request:
                if 'text' in obj_request and 'user_id' in obj_request:
                    new_place_obj = Place(**obj_request)
                    setattr(new_place_obj, "place_id", city_id)
                    new_place_obj.save()
                    return (jsonify(new_place_obj.to_dict()), 201)
                else:
                    if 'user_id' not in obj_request:
                        abort(400, "Missing user_id")
                    if 'text' not in obj_request:
                        abort(400, "Missing text")
            else:
                abort(400, "Not a JSON")
        else:
            abort(404)
    except IntegrityError:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """updates a city object"""
    place_onj = storage.get(Place, review_id)
    obj_request = request.get_json()
    if place_onj:
        if obj_request:
            for key, value in obj_request.items():
                ignore = ["id", "user_id", "city_id",
                          "created_at", "updated_at"]
                if key != ignore:
                    setattr(place_onj, key, value)
            place_onj.save()
            return jsonify(place_onj.to_dict()), 200
        else:
            return "Not a JSON", 400
    else:
        abort(404)
