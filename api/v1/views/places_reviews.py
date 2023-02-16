#!/usr/bin/python3
"""create a new view for City objects that
   handles all default RESTFul API actions:
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def getPlaceReview(place_id):
    """ gets the review of a place by Id """
    ReviewPlace = []
    places = storage.get(Place, place_id)
    if places:
        for review in places.reviews:
            ReviewPlace.append(review.to_dict())
        return jsonify(ReviewPlace)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def getReview(review_id):
    """gets the review by id """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteReview(review_id):
    """ delete a review by id"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def postPlaceReview(place_id):
    """ post a new review"""
    data = request.get_json()
    place = storage.get(Place, place_id)
    user = storage.get(User, data.get("user_id"))
    if not place:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")
    if "user_id" not in data.keys():
        abort(400, description="Missing user_id")
    if not user:
        abort(404)
    if "text" not in data.keys():
        abort(400, description="Missing text")
    data["place_id"] = place_id
    UpdatedClass = Review(**data)
    UpdatedClass.save()
    return make_response(jsonify(UpdatedClass.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def PutReview(review_id):
    """updates the reviews"""
    review = storage.get(Review, review_id)
    data = request.get_json()
    if not review:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")
    ignoreList = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignoreList:
            setattr(review, k, v)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
