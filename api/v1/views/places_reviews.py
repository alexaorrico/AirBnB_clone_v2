#!/usr/bin/python3
"""HolbertonBnB Review view."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger import swag_from
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"])
@swag_from("../apidocs/places_reviews/get_reviews.yml", methods=["GET"])
@swag_from("../apidocs/places_reviews/post.yml", methods=["POST"])
def reviews(place_id):
    """Defines the GET and POST method for reviews on /places route.

    GET - Retrieves a list of all Reviews related to a given place_id.
    POST - Creates a Review.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    # GET method
    if request.method == "GET":
        return jsonify([r.to_dict() for r in place.reviews])

    # POST method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    user_id = data.get("user_id")
    if user_id is None:
        return "Missing user_id", 400
    if storage.get("User", user_id) is None:
        abort(404)
    if data.get("text") is None:
        return "Missing text", 400
    data["place_id"] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"])
@swag_from("../apidocs/places_reviews/get_review_id.yml", methods=["GET"])
@swag_from("../apidocs/places_reviews/delete.yml", methods=["DELETE"])
@swag_from("../apidocs/places_reviews/put.yml", methods=["PUT"])
def review_id(review_id):
    """Defines the GET, PUT and DELETE methods for a specific ID on reviews.

    GET - Retrieves a Review object with the given id.
    PUT - Updates a Review object with the given id using JSON key/values.
    DELETE - Deletes a Review object with the given id.
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    # GET method
    if request.method == "GET":
        return jsonify(review.to_dict())

    # DELETE method
    elif request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({})

    # PUT method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    avoid = {"id", "user_id", "place_id", "created_at", "updated_at"}
    [setattr(review, k, v) for k, v in data.items() if k not in avoid]
    review.save()
    return jsonify(review.to_dict())
