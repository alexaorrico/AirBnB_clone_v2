#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from flasgger.utils import swag_from
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_place_reviews(place_id):
    """return a list of cities in the place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review = place.reviews
    if not review:
        abort(404)
    else:
        return jsonify([cit.to_dict() for cit in review])


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/review/get_id.yml", methods=["GET"])
def get_review_id(review_id):
    """Retrieves a specific review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    "/reviews/<string:review_id>", methods=["DELETE"], strict_slashes=False
)
@swag_from("documentation/review/delete.yml", methods=["DELETE"])
def delete_review(review_id):
    """Deletes a  review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
@swag_from("documentation/review/post_review.yml", methods=["POST"])
def post_review(place_id):
    """
    Creates a review object
    """
    if not storage.get(Place, place_id):
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    body = request.get_json()
    if "text" not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)

    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    if not storage.get(User, body.user_id):
        abort(404)

    instance = Review(**body)
    instance.place_id = place_id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/review/put_review.yml", methods=["PUT"])
def put_review(review_id):
    """put review change the values of the review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, val in dict(request.get_json()).items():
        setattr(review, key, val)

    storage.save()

    return jsonify(review.to_dict())
