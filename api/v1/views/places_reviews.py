#!/usr/bin/python3

"""
A view for Review instances that manages all standard RESTful API actions.

Authors: Khotso Selading and Londeka Dlamini
"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def reviews(place_id):
    """retrieves of a list of all place objects"""
    place_object = storage.get(Place, place_id)

    if not place_object:
        abort(404)

    return jsonify([obj.to_dict() for obj in place_object.reviews])


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_reviews(review_id):
    """retrieves specific place obj"""
    review_object = storage.get(Review, review_id)

    if not review_object:
        abort(404)

    return jsonify(review_object.to_dict())


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_review(review_id):
    """deletes specific place object"""
    review_object = storage.get(Review, review_id)

    if not review_object:
        abort(404)

    review_object.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def post_review(place_id):
    """adds new review object to filestorage/database"""
    place_object = storage.get(Place, place_id)

    if not place_object:
        abort(404)
    json_body = request.get_json()
    if json_body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if json_body.get('user_id') is None:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if storage.get(User, json_body.get('user_id')) is None:
        abort(404)
    if json_body.get('text') is None:
        return make_response(jsonify({"error": "Missing text"}), 400)

    json_body['place_id'] = place_id
    review = Review(**json_body)
    review.save()
    return make_response(jsonify(place_object.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def put_review(review_id):
    """adds new review object to filestorage/database"""
    review_object = storage.get(Review, review_id)
    json_body = request.get_json()

    if not review_object:
        abort(404)
    if json_body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in json_body.items():
        if key not in {'id', 'user_id', 'place_id',
                       'created_at', 'updated_at'}:
            setattr(review_object, key, value)

    review_object.save()
    return make_response(jsonify(review_object.to_dict()), 200)
