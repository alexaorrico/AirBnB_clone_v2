#!/usr/bin/python3
""" Module for reviews """

from models import storage
from models.review import Review
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def get_review_place(place_id):
    """Gets all reviews using place id"""
    get_pl = storage.get("Place", place_id)
    if not get_pl:
        abort(404)
    return jsonify([r.to_dict() for r in get_pl.reviews])


@app_views.route("/reviews/<review_id>", methods=['GET'])
def get_review_id(review_id):
    """
    Gets review by id
    """
    r_instance = storage.get("Review", review_id)
    if not r_instance:
        abort(404)
    return jsonify(r_instance.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_reviewid(review_id):
    """
    Deletes review using id
    """
    r_instance = storage.get("Review", review_id)
    if not r_instance:
        abort(404)
    storage.delete(r_instance)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates new Review
    """
    get_pl = storage.get("Place", place_id)
    if not get_pl:
        abort(404)
    result = request.get_json()
    if result is None:
        abort(400, 'Not a JSON')
    if 'text' not in result:
        abort(400, 'Missing text')
    if 'user_id' not in result:
        abort(400, 'Missing user_id')
    get_u = storage.get("User", result['user_id'])
    if not get_u:
        abort(404)
    instance = Review(**result)
    instance.user_id = result['user_id']
    instance.place_id = place_id
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review_id(review_id):
    """
    Updates a review with specified id
    """
    instance = storage.get("Review", review_id)
    if not instance:
        abort(404)
    result = request.get_json()
    if result is None:
        abort(400, 'Not a JSON')
    if 'text' in result:
        instance.text = result['text']
    if 'place_id' in result:
        get_p = storage.get("Place", result['place_id'])
        if not get_p:
            abort(404)
        instance.place_id = result['place_id']
    if 'user_id' in result:
        get_u = storage.get("User", result['user_id'])
        if not get_u:
            abort(404)
        instance.user_id = res['user_id']
    instance.save()
    return jsonify(instance.to_dict()), 200
