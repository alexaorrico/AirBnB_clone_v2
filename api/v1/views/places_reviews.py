#!/usr/bin/python3
""" Create a new view for Review objects that handles all
    default RESTFul API actions
"""


from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, request
from models.review import Review
from models.place import Place
from models import storage


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def review_abor(place_id=None):
    """ Retrieves the list of all place.reviews objects """
    place = storage.get("Place", place_id)
    lista = []
    if place is None:
        abort(404)
    else:
        for value in place.reviews:
            lista.append(value.to_dict())
        return jsonify(lista)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def review_abor2(review_id=None):
    """ Retrieves the list of all places objects """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def review_del(review_id=None):
    """delete a object if it is into reviews """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id=None):
    """ post method review, You must use request.get_json from Flask """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "user_id" not in json_data.keys():
        return jsonify({'error': "Missing user_id"}), 400
    if "text" not in json_data.keys():
        return jsonify({'error': "Missing text"}), 400
    user = storage.get("User", json_data['user_id'])
    if user is None:
        abort(404)
    json_data['place_id'] = place_id
    review = Review(**json_data)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id=None):
    """ method put Updates a Review object: PUT """
    p_review = storage.get("Review", review_id)
    if p_review is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key != "__class__":
            setattr(p_review, key, value)
    storage.save()
    return jsonify(p_review.to_dict()), 200
