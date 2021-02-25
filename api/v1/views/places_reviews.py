#!/usr/bin/python3
"""this is a test string"""

from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<p_id>/reviews",
                 strict_slashes=False,
                 methods=["GET", "POST"])
def reviews_base(p_id):
    """this is a test string"""
    if request.method == "GET":
        out = []
        place = storage.get(Place, p_id)
        if place:
            for review in place.reviews:
                out.append(review.to_dict())
            return jsonify(out)
        abort(404)
    if request.method == "POST":
        if not request.is_json:
            return "Not a JSON", 400
        place = storage.get(Place, p_id)
        if place:
            kwargs = {"place_id": p_id}
            kwargs.update(request.get_json())
            out = Review(**kwargs)
            info = out.to_dict()
            if "user_id" not in info.keys():
                return "Missing user_id", 400
            if not storage.get(User, info.get("user_id")):
                abort(404)
            if "text" not in info.keys():
                return "Missing text", 400
            out.save()
            return out.to_dict(), 201
        abort(404)


@app_views.route("/reviews/<r_id>",
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def reviews_id(r_id):
    """this is a test string"""
    if request.method == "GET":
        review = storage.get(Review, r_id)
        if review:
            return review.to_dict()
        abort(404)
    if request.method == "DELETE":
        review = storage.get(Review, r_id)
        if review:
            review.delete()
            storage.save()
            return {}, 200
        abort(404)
    if request.method == "PUT":
        review = storage.get(Review, r_id)
        if review:
            if not request.is_json:
                return "Not a JSON", 400
            for k, v in request.get_json().items():
                if k not in ["id", "user_id", "place_id",
                             "created_at", "updated_at"]:
                    setattr(review, k, v)
            storage.save()
            return review.to_dict(), 200
        abort(404)
