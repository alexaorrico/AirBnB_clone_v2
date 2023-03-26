#!/usr/bin/python3
"""view for Review objects that handles all default RESTFul API actions"""
from models.user import User
from flask import jsonify
from flask import abort
from flask import request
from models.review import Review
from models.place import Place
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def reviews(place_id):
    """Retrieves the list of all Review objects"""
    try:
        places = storage.get(Place, place_id)
    except:
        abort(404)
    ReviewList = []
    for review in places.reviews:
        ReviewList.append(review.to_dict())
    return jsonify(ReviewList)


@app_views.route("/reviews/<review_id>", methods=['GET'])
def getPlacesReview(review_id):
    """Retrieves a Review object"""
    try:
        review = storage.get(Review, review_id).to_dict()
        return jsonify(Review)
    except:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def deletePlacesReview(review_id):
    """Deletes a Review object"""
    try:
        storage.delete(Review, review_id)
        storage.save()
        return {}, 200
    except:
        abort(404)


@app_views.route("/places/<place_id>/reviews",
                 methods=['POST'], endpoint='reviewsPost')
def postPlacesReview(place_id):
    """Creates a Review"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    if 'text' not in data:
        abort(400, "Missing text")
    try:
        place = storage.get(Place, place_id)
        user = storage.get(User, data['user_id'])
    except:
        abort(404)
    instance = Review(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'])
def putPlacesReview(review_id):
    """Updates a Review object"""
    k = "Review." + str(review_id)
    if k not in storage.all():
        abort(404)
    data = request.get_json()
    if not request.is_json:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at',
                       'user_id', 'place_id']:
            setattr(storage.all()[k], key, value)
    storage.all()[k].save()
    try:
        return jsonify(storage.get(Review, review_id).to_dict()), 200
    except:
        abort(404)
