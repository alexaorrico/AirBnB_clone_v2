#!/usr/bin/python3
"""Flask app to handle reviews API"""
from models import storage
from models.place import Place
from models.review import Review
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """Retrieves the list of amenities"""
    amen_place = storage.get("Place", place_id)
    if amen_place is None:
        abort(404)
    amen_list = [amen.to_dict() for amen in amen_place.reviews]
    return jsonify(amen_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_reviews_by_id(review_id):
    """Retrieves a single amenity"""
    amen_obj = storage.get("Review", review_id)
    if amen_obj is None:
        abort(404)
    amen_dict = amen_obj.to_dict()
    return jsonify(amen_dict)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review"""
    rev_obj = storage.get("Review", review_id)
    if rev_obj is None:
        abort(404)
    rev_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_reviews(place_id):
    """Creates a single Review"""
    if storage.get("Place", place_id) is None:
        abort(404)
    json_rev = request.get_json()
    if not request.json:
        return jsonify("Not a JSON"), 400
    if 'user_id' not in json_rev:
        return jsonify("Missing user_id"), 400
    if storage.get("User", json_rev['user_id']) is None:
        abort(404)
    if 'text' not in json_rev:
        return jsonify("Missing text"), 400
    json_rev['place_id'] = place_id
    new_rev_obj = Review(**json_rev)
    new_rev_obj.save()
    new_rev_obj = new_rev_obj.to_dict()
    return jsonify(new_rev_obj), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review_by_id(review_id):
    """Updates a Place object"""
    rev_obj = storage.get("Review", review_id)
    if rev_obj is None:
        abort(404)
    json_obj = request.get_json()
    if not request.json:
        return jsonify("Not a JSON"), 400
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in json_obj.items():
        if key not in ignore:
            setattr(rev_obj, key, value)
    rev_obj.save()
    updated_review = rev_obj.to_dict()
    return jsonify(updated_review), 200
