#!/usr/bin/python3
"""view for Review object that handles all default RESTFul API actions"""
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import make_response
from flask import request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def getReview(place_id):
    """retrieve the list of all Review objects of a Place"""
    all_reviews = storage.all(Review)
    all_places = storage.all(Place)
    place_ids = [val.id for val in all_places.values()]
    review_list = []
    if place_id not in place_ids:
        return make_response(jsonify({"error": "Not found"}), 404)
    for val in all_reviews.values():
        print(val.id, place_id)
        if val.place_id == place_id:
            review_list.append(val.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def getReviews(review_id):
    """retrieve a Review object"""
    all_reviews = storage.all(Review)
    for val in all_reviews.values():
        if val.id == review_id:
            return jsonify(val.to_dict())
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteReview(review_id):
    """delete a review object"""
    all_reviews = storage.all(Review)
    for val in all_reviews.values():
        if val.id == review_id:
            storage.delete(val)
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def createReview(place_id):
    """create a Review"""
    all_places = storage.all(Place)
    all_users = storage.all(User)
    all_place_ids = [val.id for val in all_places.values()]
    all_user_ids = [val.id for val in all_users.values()]
    try:
        data = request.get_json()
        if place_id not in all_place_ids:
            return make_response(jsonify({"error": "Not found"}), 404)
        if "user_id" not in data:
            return make_response("Missing user_id", 400)
        if data['user_id'] not in all_user_ids:
            return make_response(jsonify({"error": "Not found"}), 404)
        if "text" not in data:
            return make_response("Missing text", 400)
        data['place_id'] = place_id
        new_review = Review(**data)
        for k, v in data.items():
            setattr(new_review, k, v)
            storage.new(new_review)
            storage.save()
            return make_response(jsonify(new_review.to_dict()), 201)
    except Exception as e:
        return make_response("Not a JSON", 400)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def updateReview(review_id):
    """update a Review object"""
    all_reviews = storage.all(Review)
    try:
        data = request.get_json()
        for val in all_reviews.values():
            if val.id == review_id:
                for k, v in data.items():
                    setattr(val, k, v)
                    storage.save()
                    return make_response(jsonify(val.to_dict()), 200)
        return make_response(jsonify({"error": "Not found"}), 404)
    except Exception as e:
        return make_response("Not a JSON", 400)
