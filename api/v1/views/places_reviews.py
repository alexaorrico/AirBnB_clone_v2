#!/usr/bin/python3
"""
flask application module for retrieval of
Review Objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review

@app_views.route('places/<string:place_id>/reviews',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """Retrieves the list of all Review objects"""
    print("in correct route")
    if request.method == 'GET':
        returnedValue, code = Review.api_get_all(
                    storage.get("Place", place_id).reviews)
    if request.method == 'POST':
        returnedValue, code = Review.api_post(
                    ["user_id", "text"],
                    request.get_json(silent=True),
                    place_id)
    if code == 404:
        abort(404)
    storage.save()
    return (jsonify(returnedValue), code)


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def Review_by_id(review_id):
    """handles Review object: Review_id"""
    if request.method == 'GET':
        returnedValue, code = Review.api_get_single(
                        storage.get("Review", review_id))
    if request.method == 'DELETE':
        returnedValue, code = Review.api_delete(
                    storage.get("Review", review_id))
    if request.method == 'PUT':
        returnedValue, code = Review.api_put(
                    ['id', 'user_id', 'place_id', 'created_at', 'updated_at'],
                    request.get_json(silent=True),
                    storage.get("Review", review_id))
    if code == 404:
        abort(404)
    storage.save()
    return (jsonify(returnedValue), code)
