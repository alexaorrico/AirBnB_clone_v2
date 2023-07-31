#!/usr/bin/python3
"""
A new view for Place objects that handles all default RESTFul API actions
"""
from flask import abort
from flask import jsonify
from flask import request

from . import User
from . import Place
from . import Review
from . import storage
from . import app_views

f = ("user_id", "text")


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET", "POST"], strict_slashes=False)
def reviews_by_place(place_id):
    """
    Creates a new Review object
    Retrieves the list of all Review objects of a Review
    Args:
        place_id: primary key of an existing Review object
    """
    place = storage.get(Place, str(place_id))
    if place is None:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify([r.to_dict() for r in place.reviews])
    else:
        body = request.get_json(silent=True)
        if request.is_json and body is not None:
            pay = {k: str(v) for k, v in body.items() if k in f}
            for k in f:
                if not pay.get(k, None):
                    abort(400, description="Missing " + k)
                if k == "user_id" and\
                        not storage.get(User, str(pay.get("user_id"))):
                    abort(404, description="Not found")
            pay.update({"place_id": place_id})
            new_review = Review(**pay)
            storage.new(new_review), storage.save()
            return jsonify(new_review.to_dict()), 201
        abort(400, description="Not a JSON")


@app_views.route("/reviews/<review_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def one_review(review_id):
    """
    Deletes an existing Review object
    Retrieves an existing Review object
    Updates an existing Review object
    Args:
        review_id: primary key of an existing Review object
    """
    review = storage.get(Review, str(review_id))
    if not review:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(review.to_dict())
    elif request.method == "DELETE":
        storage.delete(review), storage.save()
        return jsonify({})
    else:
        body = request.get_json(silent=True)
        if request.is_json and body is not None:
            [setattr(review, k, str(v))
                for k, v in body.items() if k in f[1:]]
            review.save()
            return jsonify(review.to_dict()), 200
        abort(400, description="Not a JSON")
