#!/usr/bin/python3
""" new view for Review objects """

from models.place import Place
from models.user import User
from models.review import Review
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage, base_model


@app_views.route(
    '/places/<place_id>/reviews',
    strict_slashes=False,
    methods=['GET']
)
def get_reviews(place_id):
    """Retrieves the list of all Reviews objects"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    else:
        review_list = []
        for review in place.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """Get review by its id"""
    review_id = storage.get(Review, review_id)
    if review_id is None:
        return abort(404)
    return jsonify(review_id.to_dict())


@app_views.route(
    '/reviews/<review_id>',
    strict_slashes=False,
    methods=['DELETE']
)
def delete_review_ob(review_id):
    """Delete a Review object by id"""
    review_id = storage.get(Review, review_id)
    if review_id is None:
        return abort(404)
    else:
        storage.delete(review_id)
        storage.save()
        return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/reviews',
    strict_slashes=False,
    methods=['POST']
)
def create_review_ob(place_id):
    """Create a Review object by place id"""
    if request.method == 'POST':
        place = storage.get(Place, place_id)
        data = request.get_json()
        if not place:
            return abort(404)
        if not data:
            return 'Not a JSON', 400
        if "user_id" not in data:
            return 'Missing user_id', 400
        user = storage.get(User, data.get("user_id"))
        if not user:
            return abort(404)
        elif "text" not in data:
            return 'Missing text', 400
        else:
            ob = Review(**data)
            # ob.review_id = review_id
            ob.place_id = place_id
            storage.new(ob)
            storage.save()
            return(jsonify(ob.to_dict())), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review_ob(review_id):
    """Update a review object"""
    if request.method == 'PUT':
        ob = storage.get(Review, review_id)
        data = request.get_json()
        if not ob:
            return abort(404)
        if not data:
            return "Not a JSON", 400
        list_keys = [
            "id", "user_id",
            "place_id",
            "created_at",
            "updated_at"
        ]
        for key, val in data.items():
            if key not in list_keys:
                setattr(ob, key, val)
        storage.save()
        return jsonify(ob.to_dict()), 200
