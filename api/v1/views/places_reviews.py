#!/usr/bin/python3
"""adasda"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models import review
from models import place
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def getCity(place_id):
    """aaasdasdasd"""
    reviews = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def getCityById(review_id):
    """asdasdasda"""
    review = storage.get(Place, review_id)
    if review is None:
        abort(404)
    review = review.to_dict()
    return jsonify(review)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteCity(review_id):
    """asdasdasda"""
    review = storage.get(Place, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def CreateCity(place_id):
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    if json_req.get("name") is None:
        abort(400, 'Missing name')
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_req['place_id'] = place.id
    new_obj = Review(**json_req)
    new_obj.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def updateCity(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    for key, value in json_req.items():
        if key not in ["id", "created_at", "updated_at", "user_id"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
