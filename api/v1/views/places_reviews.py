#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"],
                 strict_slashes=False)
def get_reviews(place_id):
    res = []
    Place = storage.get(Place, place_id)
    if Place is None:
        abort(404)
    if request.method == "GET":
        for review in Place.reviews:
            res.append(review.to_dict())
        return (jsonify(res))
    if request.method == "POST":
        if not request.json:
            abort(400, description="Not a JSON")
        if "user_id" not in request.json:
            abort(400, description="Missing user_id")
            user_id = request.json["user_id"]
            user = storage.get(User, user_id)
            if user is None:
                abort(404)
        if "text" not in request.json:
            abort(400, description="Missing text")
            user_id = request.json["user_id"]
            text = request.json["text"]
            new_review = Review(user_id=user_id, text=text)
            new_review.save()
            return (jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=True)
def manage_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    if request.method == "PUT":
        if not request.json:
            abort(400, description="Not a JSON")
        for key, value in request.json.items():
            setattr(review, key, value)
        review.save()
        return (jsonify(review.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
