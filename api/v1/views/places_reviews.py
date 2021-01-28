#!/usr/bin/python3
"""Reviews"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route('/place/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def place_getplacerev(place_id=None):
    """Retrieve reviews from each place"""
    state = storage.get(Place, place_id)
    if state is None:
        abort(404)
    list_review = []
    for i in state.places_reviews:
        list_review.append(i.to_dict())
    return jsonify(list_review)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    """get city objects"""
    vrev = storage.get(Review, review_id)
    if vrev is None:
        abort(404)
    else:
        return jsonify(vrev.to_dict())


@app_views.route('/reviews/<review_id>>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id=None):
    """Delete review"""
    if storage.get(Review, review_id):
        storage.delete(storage.get(Review, review_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ post method """
    if storage.get(Place, place_id) is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    elif "user_id" not in data.keys():
        abort(400, "Missing user_id")
    elif not storage.get("User", data["user_id"]):
        abort(404)
    elif "text" not in data.keys():
        abort(400, "Missing text")
    else:
        new_rev = Review(**data)
        storage.save()
    return jsonify(new_rev.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id=None):
    """Put method"""
    data = request.get_json()
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    if data is None:
        return "Not a JSON", 400
    for k, v in data.items():
        if k in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            pass
        else:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
