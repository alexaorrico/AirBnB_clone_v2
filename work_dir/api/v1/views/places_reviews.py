#!/usr/bin/python3
"""

Flask web server creation to handle api petition-requests

"""
from flask import jsonify, abort
from flask import request
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def all_reviews(place_id):
    """
    Retrieves the list of all review objects
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)
    my_list = []
    for review in place.reviews:
        my_list.append(review.to_dict())
    return jsonify(my_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def some_review(review_id):
    """
    Retrieves a Review object if id is linked to some Review object
    """
    some_objs = storage.get(classes["Review"], review_id)
    if some_objs is None:
        abort(404)
    some_objs = some_objs.to_dict()
    return jsonify(some_objs)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_review(review_id):
    """
    Deletes a Review object if id is linked to some Review object
    """
    some_objs = storage.get(classes["Review"], review_id)
    if some_objs is None:
        abort(404)
    storage.delete(some_objs)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def post_review(place_id):
    """
    Create a new Review object
    """
    place_obj = storage.get(classes["Place"], place_id)
    if place_obj is None:
        abort(404)
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    if "user_id" not in data_json:
        abort(400, "Missing user_id")
    user_obj = storage.get(classes["User"], data_json["user_id"])
    if user_obj is None:
        abort(404)
    if "text" not in data_json:
        abort(400, "Missing text")
    else:
        new_review = classes["Review"](place_id=place_id, **data_json)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def put_review(review_id):
    """
    Update a Review object
    """
    obj = storage.get(classes["Review"], review_id)
    if obj is None:
        abort(404)
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    for key, value in data_json.items():
        if key in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            continue
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
