#!/usr/bin/python3
"""
Handles all default RESTful API actions for Place objects
"""

from . import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from flask import abort, jsonify, make_response, request

REVIEW_IGNORE_KEYS = {'id', 'user_id', 'place_id', 'created_at', 'updated_at'}


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def get_places_reviews(place_id):
    """Retrieves the list of all Reviews objects attached to a Place"""
    p = storage.get('Place', place_id)
    if p is None:
        abort(404)
    return jsonify([r.to_dict() for r in p.reviews])


@app_views.route("/reviews/<review_id>", methods=['GET'])
def get_review(review_id):
    """Retrieves a review given its ID"""
    r = storage.get('Review', review_id)
    if r is None:
        abort(404)
    return jsonify(r.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def del_review(review_id):
    """Deletes a review given its ID"""
    r = storage.get('Review', review_id)
    if r is None:
        abort(404)
    r.delete()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=['POST'])
def post_review(place_id):
    """Creates a review"""
    p = storage.get('Place', place_id)
    if p is None:
        abort(404)
    r = request.get_json()
    if r is None:
        abort(make_response(jsonify("Not a JSON"), 400))
    if 'user_id' not in r:
        abort(make_response(jsonify("Missing user_id"), 400))
    u = storage.get('User', r['user_id'])
    if u is None:
        abort(404)
    if 'text' not in r:
        abort(make_response(jsonify("Missing text"), 400))
    r['place_id'] = place_id
    rev = Review(**r)
    rev.save()
    return make_response(jsonify(rev.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'])
def put_review(review_id):
    """Updates a Review given its ID"""
    rev = storage.get('Review', review_id)
    if rev is None:
        abort(404)
    r = request.get_json()
    if r is None:
        abort(make_response(jsonify("Not a JSON"), 400))
    for k, v in r.items():
        if k not in REVIEW_IGNORE_KEYS:
            setattr(rev, k, v)
    rev.save()
    return make_response(jsonify(rev.to_dict()), 200)
