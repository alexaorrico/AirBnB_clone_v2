#!/usr/bin/python3
""" Methos API for object Place-Reviews """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models import place
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_place_review(place_id):
    """ Get Reviews objects of Places """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """ Get one Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ Create a new Review object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    request_review = request.get_json()
    if not request_review:
        abort(400, "Not a JSON")
    if "user_id" not in request_review:
        abort(400, "Missing user_id")
    user_id = request_review['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if "text" not in request_review:
        abort(400, "Missing text")
    review = Review(**request_review)
    review.place_id = place_id
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """ Update a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    request_review = request.get_json()
    if not request_review:
        abort(400, "Not a JSON")

    for key, value in request_review.items():
        if key not in [
                        'id', 'user_id', 'place_id',
                        'created_at', 'updated_at'
                    ]:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
