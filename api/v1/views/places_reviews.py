#!/usr/bin/python3
"""A new view for Review objects that handles all default RESTFUL
API actions"""


from flask import Flask, jsonify, request, abort
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    """Retrives all Review objects in the storage
    given a place id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [r.to_dict() for r in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_based_on_id(review_id):
    """Retrives a Review object given it's id else return 404
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review_object(review_id):
    """Deletes a Review object if found otherwise return 404
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review_object(place_id):
    """Creates a Review object returns the created object
    """
    lista = []
    obj = storage.get("Place", place_id)
    content = request.get_json()
    if not obj:
        abort(404)
    if not request.json:
        return (jsonify("Not a JSON"), 400)
    else:
        if "user_id" not in content.keys():
            return (jsonify("Missing user_id"), 400)
        obj2 = storage.get("User", content["user_id"])
        if not obj2:
            abort(404)
        if "text" not in content.keys():
            return (jsonify("Missing text"), 400)

        content["place_id"] = place_id
        new_place = Review(**content)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a Review object based on the id
    """

    fetch_r = storage.get(Review, review_id)
    if not fetch_r:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    keep = ["id", "created_at", "updated_at", "user_id", "place_id"]
    for key, values in data.items():
        if key not in keep:
            setattr(fetch_r, key, values)

    fetch_r.save()
    return jsonify(fetch_r.to_dict()), 200
