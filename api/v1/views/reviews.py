#!/usr/bin/python3
""" flask module to manage the stored reviews """
from models.review import Review
from models.place import Place
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage


@app_views.route(
    '/places/<string:place_id>/reviews',
    strict_slashes=False,
    methods=['GET']
)
def all_reviews(place_id):
    """ it retrieve all the reviews """
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    reviews_list = []
    for review in places.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route(
    '/reviews/<string:review_id>',
    strict_slashes=False,
    methods=['GET']
)
def get_review(review_id):
    """ it get the review corresponding to the review_id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    '/reviews/<string:review_id>',
    strict_slashes=False,
    methods=['DELETE']
)
def delete_review(review_id):
    """ it delete the review corresponding to the review_id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/places/<string:place_id>/reviews',
    strict_slashes=False,
    methods=['POST']
)
def create_review(place_id):
    """ it create an review from a http request
    the new review information is expected to be
    json string
    """
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    review_json = request.get_json()
    if review_json is None:
        abort(400, 'Not a JSON')
    if review_json.get('user_id') is None:
        abort(400, "Missing user_id")
    if review_json.get('text') is None:
        abort(400, "Missing text")
    review = Review(**review_json)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route(
    '/reviews/<string:review_id>',
    strict_slashes=False, methods=['PUT']
)
def update_review(review_id):
    """ it update an review """
    ignored_keys = ['id', 'user_id', 'created_at', 'place_id']
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review_json = request.get_json()
    if review_json is None:
        abort(400, 'Not a JSON')

    for key in review_json.keys():
        if key in ignored_keys:
            continue
        if getattr(review, key):
            setattr(review, key, review_json[key])
    storage.save()
    return jsonify(review.to_dict()), 200
