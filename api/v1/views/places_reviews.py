#!/usr/bin/python3
""" places_reviews module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """ get list of all Reviews """
    all_reviews = []
    if not storage.get('Place', place_id):
        abort(404)
    for review in storage.all('Review').values():
        if place_id == review.to_dict()['place_id']:
            all_reviews.append(review.to_dict())
    return jsonify(all_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_review(review_id):
    """ get a single Review """
    review = storage.get('Review', review_id)
    if review:
        return review.to_dict()
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ delete an Review """
    review = storage.get('Review', review_id)
    if review:
        storage.delete(review)
        storage.save()
        return {}
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ create a Review """
    review_name = request.get_json()
    if not storage.get('Place', place_id):
        abort(404)
    if not review_name:
        abort(400, {'Not a JSON'})
    elif 'user_id' not in review_name:
        abort(400, {'Missing user_id'})
    elif not storage.get('User', review_name['user_id']):
        abort(404)
    elif 'text' not in review_name:
        abort(400, {'Missing text'})
    review_name['place_id'] = place_id
    new_review = Review(**review_name)
    storage.new(new_review)
    storage.save()
    return new_review.to_dict(), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ update a Review """
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    my_review = storage.get('Review', review_id)
    if not my_review:
        abort(404)
    for key, value in update_attr.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(my_review, key, value)
    storage.save()
    return my_review.to_dict()
