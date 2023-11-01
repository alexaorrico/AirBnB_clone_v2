#!/usr/bin/python3
"""reviews for the place uisng review_id and place_id"""

from flask import jsonify, request, abort
from . import app_views, Place, Review, storage, User

pl = ("user_id", "text")


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET", "POST"], strict_slashes=False)
def post_placeid(place_id):
    """Adds new pid to the ls of reviews associated with the given place id"""
    pid = storage.get(Place, str(place_id))
    if pid is None:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify([list.to_dict() for list in pid.reviews])
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            load = {key: str(value) for key, value in data.items()
                    if key in pl}
            for key in pl:
                if not load.get(key, None):
                    abort(400, description="Missing " + key)
                if key == "user_id" and\
                        not storage.get(User, str(load.get("user_id"))):
                    abort(404, description="Not found")
            load.update({"place_id": place_id})
            added_review = Review(**load)
            storage.new(added_review), storage.save()
            return jsonify(added_review.to_dict()), 201
        abort(400, description="Not a JSON")


@app_views.route("/reviews/<review_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def delete_reviewid(review_id):
    """"Removes a review from the list linked to the given review_id"""
    deleted_rid = storage.get(Review, str(review_id))
    if not deleted_rid:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(deleted_rid.to_dict())
    elif request.method == "DELETE":
        storage.delete(deleted_rid), storage.save()
        return jsonify({})
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            [setattr(deleted_rid, key, str(value))
                for key, value in data.items() if key in pl[1:]]
            deleted_rid.save()
            return jsonify(deleted_rid.to_dict()), 200
        abort(400, description="Not a JSON")
