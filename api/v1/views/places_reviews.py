#!/usr/bin/python3
'''
    RESTful API for class Review
'''
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_by_place(place_id):
    ''' returns reviews with maching place id using json format '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    review_list = [rev.to_dict() for rev in place.reviews]
    return jsonify(review_list), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    ''' find and returns review with maching id '''
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    ''' deletes review object with maching review_id '''
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_new_review(place_id):
    '''
        create new review obj through place association using POST
    '''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif storage.get("Place", place_id) is None:
        abort(404)
    elif "user_id" not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    elif storage.get("User", data["user_id"]) is None:
        abort(404)
    elif "text" not in data:
        return make_response(jsonify({"error": "Missing text"}), 400)
    else:
        obj = Review(**data)
        obj.place_id = place_id
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    ''' updates review object using given id '''
    data = request.get_json()
    obj = storage.get("Review", review_id)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif obj is None:
        abort(404)
    else:
        keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        for key in data.keys():
            if key not in keys:
                setattr(obj, key, data[key])
        obj.save()
        return jsonify(obj.to_dict()), 200
