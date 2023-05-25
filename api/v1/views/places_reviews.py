#!/usr/bin/python3
""" Configures RESTful api for the reviews route """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route("places/<place_id>/reviews", methods=["GET", "POST"],
                 strict_slashes=False)
def reviews(place_id):
    """ configures the reviews route """

    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    if request.method == "GET":
        reviews_dict = [review.to_dict() for review in place.reviews]

        return jsonify(reviews_dict)
    else:
        try:
            json_dict = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        try:
            user_id = json_dict["user_id"]
        except KeyError:
            abort(400, "Missing user_id")

        user = storage.get("User", user_id)
        if not user:
            abort(404)

        try:
            text = json_dict["text"]
        except KeyError:
            abort(400, "Missing text")

        new_review = Review()
        new_review.user_id = user_id
        new_review.place_id = place_id
        new_review.text = text

        storage.new(new_review)
        storage.save()

        return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def reviews_id(review_id):
    """ configures the reviews/<review_id> route """

    review = storage.get("Review", review_id)

    if not review:
        abort(404)

    if request.method == "GET":
        return jsonify(review.to_dict())
    elif request.method == "DELETE":
        storage.delete(review)
        storage.save()

        return jsonify({}), 200
    else:
        try:
            json_dict = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        keys_to_ignore = [
                "id", "user_id", "place_id",
                "created_at", "updated_at"
        ]
        for key, val in json_dict.items():
            if key not in keys_to_ignore:
                setattr(review, key, val)

        storage.new(review)
        storage.save()

        return jsonify(review.to_dict()), 200
