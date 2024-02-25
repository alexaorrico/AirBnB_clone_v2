#!/usr/bin/python3
"""
Places_reviews View
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views('/places/<place_id>/reviews', methods=["GET"],
           strict_slashes=False)
def get_reviews(place_id):
    """Gets all Reviews by using Place ID"""
    fecthed_city = storage.get("Place", str(place_id))
    if fecthed_city is None:
        abort(404)

    places_list = []
    for obj in fecthed_city.places:
        places_list.append(obj.to_dict())

    resp = jsonify(places_list)
    return resp


@app_views('/reviews/<review_id>', methods=['GET'],
           strict_slashes=False)
def get_review(review_id):
    """Gets Review using an ID"""
    fetched_place = storage.get('Review', str(review_id))
    if fetched_place is None:
        abort(404)
    resp = jsonify(fetched_place.to_dict())
    return resp


@app_views('/reviews/<review_id>', methods=['DELETE'],
           strict_slashes=False)
def delete_review(review_id):
    """Deletes a review based on the ID"""
    fetched_place = storage.get("Review", str(review_id))
    if fetched_place is None:
        abort(404)
    storage.delete(fetched_place)
    storage.save()
    return ({}, 200)


@app_views('/places/<place_id>/reviews', methods=['POST'],
           strict_slashes=False)
def create_review(place_id):
    """Creates a review using place ID"""
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("Place", str(place_id)):
        abort(404)

    if not storage.get("User", review_json["user_id"]):
        abort(404)

    if "text" not in review_json:
        abort(400, 'Missing text')

    if "user_id" not in review_json:
        abort(400, "Missing user_id")

    review_json["place_id"] = place_id

    new_review = Review(**review_json)
    new_review.save()
    resp = jsonify(new_review.to_dict())
    resp.status_code = 201

    return resp


@app_views('/reviews/<review_id>', methods=['PUT'],
           strict_slashes=False)
def updates_review(review_id):
    """Updates a Review"""
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("Review", str(review_id))
    if fetched_obj is None:
        abort(404)
    for k, val in review_json.items():
        if k not in ["id", "created_at", "updated_at", "user_id", "place_id"]:
            setattr(fetched_obj, k, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict())
