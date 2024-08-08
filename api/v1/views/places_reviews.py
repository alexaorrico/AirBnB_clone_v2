#!/usr/bin/python3
"""modify place objects via APIs"""
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from flask import jsonify, make_response, abort, request
from models import storage
from api.v1.views import app_views


def abortNotExists(cls, obj_id):
    """exit with a 404 status if obj not found"""
    obj = storage.get(cls, obj_id)
    if obj is None:
        abort(404)
    return obj


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=["GET"])
def get_place_reviews(place_id=None):
    """
    Retrieves the list of all Review objects of a Place:
    GET /api/v1/places/<place_id>/reviews
    """
    place = abortNotExists(Place, place_id)
    reviews_dicts_list = []
    for review in place.reviews:
        reviews_dicts_list.append(review.to_dict())
    return jsonify(reviews_dicts_list)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["GET"])
def get_reviews(review_id):
    """Retrieves a Review object. : GET /api/v1/reviews/<review_id>"""
    obj = abortNotExists(Review, review_id)
    return jsonify(obj.to_dict())


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=["POST"])
def post_reviews(place_id):
    """Creates a Review: POST /api/v1/places/<place_id>/reviews"""
    abortNotExists(Place, place_id)
    try:
        data = request.get_json()
        data["place_id"] = place_id
    except Exception:
        abort(400, description="Not a JSON")
    if "user_id" not in data.keys():
        abort(400, description="Missing user_id")

    abortNotExists(User, data["user_id"])  # check for user id if it exists
    if "text" not in data.keys():
        abort(400, description="Missing text")

    new_obj = Review(**data)
    storage.new(new_obj)
    storage.save()
    return make_response(new_obj.to_dict(), 201)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_review(review_id):
    """DELETE a review: /api/v1/reviews/<review_id>"""
    obj = abortNotExists(Review, review_id)
    storage.delete(obj)
    storage.save()
    return make_response({}, 200)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def put_review(review_id):
    """Updates a Review object: PUT /api/v1/reviews/<review_id>"""
    obj = abortNotExists(Review, review_id)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    for key, val in data.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(obj, key, val)

    storage.save()
    return make_response(obj.to_dict(), 200)
