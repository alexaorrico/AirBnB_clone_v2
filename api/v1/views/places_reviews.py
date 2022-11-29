#!/usr/bin/python3
"""module places_review
Handles states objects for RestfulAPI
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<places_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_places(place_id):
    """Retrieves the list of all review objects of a place"""
    place_dict = storage.all(Place)
    review_list = None
    return_list = []
    for place in place_dict.values():
        if place.id == place_id:
            review_list = place.reviews
    if review_list is None:
        abort(404)
    for review in review_list:
        return_list.append(review.to_dict())
    return jsonify(return_list)


@app_views.route("/reviews/<string:review_id>", methods=["GET"],
                 strict_slashes=False)
def review_get(review_id):
    """review_get"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/review/<string:review_id>", methods=["DELETE"],
                 strict_slashes=False)
def review_delete(review_id):
    """review_delete"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<string:place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def review_post(place_id):
    """review_post"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    review_kwargs = request.get_json()
    if "user_id" not in review_kwargs:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    review = request.get_json()
    user = storage.get(User, review['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request.get_json():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    else:
        review['place_id'] = place_id
        new_review = Review(**review_kwargs)
        new_review.save()
        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<string:review_id>", methods=["PUT"],
                 strict_slashes=False)
def review_put(review_id):
    """review_put"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in request.get_json().items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
