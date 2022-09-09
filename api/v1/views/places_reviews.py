#!/usr/bin/python3
"""
Reviews instance
"""


from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_place(place_id):
    """Retrieves the list of all Review objects of a Place"""

    reviews = []
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    for review in place.reviews:
        reviews.append(review.to_dict())

    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def review_obj(review_id):
    """Retrieves a Review object"""

    review = storage.get("Review", review_id)

    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    body = request.get_json()

    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "user_id" not in body.keys():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    elif "text" not in body.keys():
        return make_response(jsonify({"error": "Missing text"}), 400)

    if storage.get("User", body["user_id"]) is None:
        abort(404)

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    else:
        review = Review(**body)
        review.place_id = place_id
        review.save()
        return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["POST"],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""

    body = request.get_json()
    no_update = ["id", "user_id", "place_id", "created_at", "updated_at"]

    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if storage.get("Review", body["review_id"]) is None:
        abort(404)

    review = storage.get("Review", review_id)

    if review is None:
        abort(404)
    else:
        for key, value in body.items():
            if key not in no_update:
                setattr(review, key, value)
            else:
                pass

        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
