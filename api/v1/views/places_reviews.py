#!/usr/bin/python3
""" handles all default RestFul API """

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models.review import Review
from models.user import User
from models.place import Place
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=["GET"],
                 strict_slashes=False)
def review_view(place_id):
    """ return a jsonified review objects """
    get_id = storage.get(Place, place_id)
    if get_id is None:
        abort(404)
    review_dict = storage.all(Review)
    review_list = []
    for value in review_dict.values():
        if value.place_id == place_id:
            review_list.append(value.to_dict())
    return (jsonify(review_list))


@app_views.route('/reviews/<review_id>', methods=["GET"], strict_slashes=False)
def reviews_id_view(review_id):
    """ returns a jsonified review obj by review_id """
    get_id = storage.get(Review, review_id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/reviews/<review_id>', methods=["DELETE"],
                 strict_slashes=False)
def review_delete(review_id):
    """ delete review obj by review_id """
    get_id = storage.get(Review, review_id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """ creating a review object """
    get_id = storage.get(Place, place_id)
    if get_id is None:
        abort(404)
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    if "user_id" not in data_req.keys():
        return (make_response(jsonify({'error': 'Missing user_id'}), 400))
    userId = storage.get(User, data_req["user_id"])
    if userId is None:
        abort(404)
    if "text" not in data_req.keys():
        return (make_response(jsonify({'error': 'Missing text'}), 400))
    data_req["place_id"] = place_id
    new_review_obj = Review(**data_req)
    new_review_obj.save()
    return (jsonify(new_review_obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """ updating a review object """
    get_id = storage.get(Review, review_id)
    if get_id is None:
        abort(404)
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    for key, value in data_req.items():
        ignore_keys = ["id", "created_at", "updated_at", "place_id", "user_id"]
        if key not in ignore_keys:
            setattr(get_id, key, value)
    get_id.save()
    return (jsonify(get_id.to_dict()), 200)
