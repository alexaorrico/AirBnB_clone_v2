#!/usr/bin/python3
"""Contains functions that Handle all requests to the reviews endpoint."""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import place, review, storage, user


@app_views.route("/reviews", strict_slashes=False,
                 defaults={'review_id': None},
                 methods=['GET'])
@app_views.route("/review/<review_id>",  methods=['GET', 'DELETE', 'PUT'])
def get_reviews(review_id):
    """Handles get, delete and put requests to the reviews endpoint."""
    if request.method == "GET":
        if review_id is None:
            return  [am_obj.to_dict() for am_obj in\
                    storage.all(review.Review).values()]
        elif review_id is not None:
            am_obj = storage.get("Review", review_id)
            if not am_obj:
                abort(404)
            return am_obj.to_dict()
    elif request.method == "PUT":
        try:
            put_data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)
        am_obj = storage.get("Review", review_id)
        if not am_obj:
            abort(404)
        for key, value in put_data.items():
            if key not in ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']:
                setattr(am_obj, key, value)
        am_obj.save()
        return make_response(jsonify(am_obj.to_dict()), 200)
    elif request.method == "DELETE":
        am_obj = storage.get("Place", place_id)
        if not am_obj:
            abort(404)
        place_obj.delete()
        storage.save()
        return (jsonify({}))


@app_views.route("/places/<place_id>/reviews", strict_slashes=False, methods=["GET"])
def get_place_review(place_id):
    """Handle get request to place reviews."""
    if place_id:
        p_obj = storage.get("Place", place_id)
        if not p_obj:
            abort(404)
        pl_rv = [obj.to_dict() for obj in storage.all(review.Review).values()\
                if obj.place_id == place_id]
        return pl_rv


@app_views.route("/places/<place_id>/reviews", strict_slashes=False, methods=["POST"])
def post_place_review(place_id):
    """Handle post request to place reviews."""
    pl_obj = storage.get("Place", place_id)
    if not pl_obj:
        abort(404)
    try:
        post_data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)
    if 'user_id' not in post_data:
        return make_response("Missing user_id", 400)
    u_obj = storage.get("User", post_data["user_id"])
    if not u_obj:
        abort(404)
    if "text" not in post_data:
        return make_response("Missing text", 400)
    new_review = review.Review()
    new_review.review_id = place_id
    new_review.text = post_data['text']
    new_review.user_id = post_data['user_id']
    new_review.save()
    return make_response(new_review.to_dict(), 201)
