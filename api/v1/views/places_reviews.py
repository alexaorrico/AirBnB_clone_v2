#!/usr/bin/python3
"""
module for review views
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews(place_id):
    """ Retrieves the list of all Place's reviews objects """
    places = storage.all("Place")
    response = []
    for key in places.keys():
        if key.split('.')[-1] == place_id:
            list_reviews = places.get(key).reviews
            for review in list_reviews:
                response.append(review.to_dict())
            return jsonify(response)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object """
    reviews = storage.all("Review")
    for key in reviews.keys():
        if key.split('.')[-1] == review_id:
            return jsonify(reviews.get(key).to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    reviews = storage.all("Review")
    for key in reviews.keys():
        if key.split('.')[-1] == review_id:
            storage.delete(reviews.get(key))
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ Creates a Review """
    dic = request.get_json()
    if not dic:
        abort(400, "Not a JSON")
    if not ('user_id' in dic.keys()):
        abort(400, "Missing user_id")
    if not ('text' in dic.keys()):
        abort(400, "Missing text")
    places = storage.all('Place')
    for key in places.keys():
        if key.split('.')[-1] == place_id:
            users = storage.all('User')
            for k in users.keys():
                if k.split('.')[-1] == dic.get('user_id'):
                    review = Review(place_id=place_id, **dic)
                    review.save()
                    return jsonify(review.to_dict()), 201
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """ Updates a Review object """
    reviews = storage.all("Review")
    review = None
    for key in reviews.keys():
        if key.split('.')[-1] == review_id:
            review = reviews.get(key)
    if not review:
        abort(404)
    new_dict = request.get_json()
    if not new_dict:
        abort(400, "Not a JSON")
    for key, value in new_dict.items():
        if key in ('id', 'user_id', 'place_id', 'created_at', 'updated_at'):
            continue
        else:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
