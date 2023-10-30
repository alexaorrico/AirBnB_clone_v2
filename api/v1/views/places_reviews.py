#!/usr/bin/python3
"""Reviews"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""

    PlaceId = storage.get('Place', place_id)
    if PlaceId is None:
        abort(404)

    dic = []

    for PlaceId in PlaceId.reviews:
        dic.append(PlaceId.to_dict())
    return jsonify(dic)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves Review """

    rID = storage.get('Review', review_id)

    if rID is None:
        abort(404)
    return jsonify(rID.to_dict())


@app_views.route('/reviews/<review_id>', methods=['Delete'],
                 strict_slashes=False)
def delete_review_places_by_id(review_id):
    """Deletes Review """

    rID = storage.get('Review', review_id)

    if rID is None:
        abort(404)

    storage.delete(rID)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_a_review(place_id):
    """Creates a Review"""

    if not storage.get("Place", place_id):
        abort(404)

    jsonI = request.get_json()

    if not jsonI:
        abort(400, 'Not a JSON')

    if "user_id" not in jsonI:
        abort(400, 'Missing user_id')

    if storage.get("User", jsonI["user_id"]) is None:
        abort(404)

    if "text" not in jsonI:
        abort(400, 'Missing text')

    review = Review(user_id=jsonI["user_id"],
                    text=jsonI["text"],
                    place_id=place_id)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_a_review_place(review_id):
    """Updates a Review object"""

    rId = storage.get('Review', review_id)

    if rId is None:
        abort(404)

    jsonI = request.get_json()

    if jsonI is None:
        abort(400, "Not a JSON")

    for key, value in jsonI.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(rId, key, value)
    storage.save()
    return jsonify(rId.to_dict()), 200
