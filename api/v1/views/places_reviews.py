#!/usr/bin/python3
"""restful API functions for Place"""
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from flask import request, jsonify, abort


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=["GET", "POST"]
                 )
def places_end_points(place_id):
    """place objects that handles all default RESTFul API actions"""
    obj_places = storage.all(Place)
    places_dict = [obj.to_dict() for obj in obj_places.values()]
    if request.method == "GET":
        for obj in places_dict:
            if obj.get('id') == place_id:
                obj_reviews = storage.all(Review)
                reviews_dict = [obj.to_dict() for obj in
                               obj_reviews.values() if
                               obj.place_id == place_id]
                return jsonify(reviews_dict)
        abort(404)

    elif request.method == "POST":
        for obj in places_dict:
            if obj.get('id') == place_id:
                my_dict = request.get_json()
                if not my_dict or type(my_dict) is not dict:
                    abort(400, "Not a JSON")
                if not my_dict["name"]:
                    abort(400, "Missing name")
                if not my_dict.get('user_id'):
                    abort(400, "Missing user_id")
                if not my_dict.get('text'):
                    abort(400, "Missing text")
                user_obj = storage.all(User).values()
                user_exists = False
                for user_obj in user_objs:
                    if user_obj.id == my_dict["user_id"]:
                        user_exists = True
                        break
                if not user_exists:
                    abort(404)
                else:
                    my_dict["place_id"] = place_id
                    new_review = Review(**my_dict)
                    new_review.save()
                    return jsonify(new_review.to_dict()), 201
        abort(404)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False,
                 methods=["DELETE", "PUT", "GET"])
def review_end_points(review_id):
    """place objects that handles all default RESTFul API actions"""
    obj_review = storage.get(Review, review_id)
    if not obj_review:
        abort(404)

    if request.method == "GET":
        return jsonify(obj_review.to_dict())
    elif request.method == "DELETE":
        storage.delete(obj_review)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        get_new_name = request.get_json()
        if not get_new_name or type(get_new_name) is not dict:
            abort(400, "Not a JSON")
        obj_review.__dict__.update(get_new_name)
        obj_review.save()
        return jsonify(obj_review.to_dict()), 201
