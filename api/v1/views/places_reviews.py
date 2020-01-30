#!/usr/bin/python3
""" This module starts the flask application for Reviews"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_places_id_reviews(place_id):
    """ GET method to list every review of a place """
    catch_place_review = storage.get('Place', place_id)
    if catch_place_review is None:
        abort(404)
    place_review_list = []
    for place_review in catch_place_review.reviews:
        place_review_list.append(place_review.to_dict())
    return jsonify(place_review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_reviews_id(review_id):
    """ GET method to list every review """
    catch_review = storage.get('Review', review_id)
    if catch_review is None:
        abort(404)
    return jsonify(catch_review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review_id(review_id):
    """ DELETE method to review a review by id """
    catch_review = storage.get('Review', review_id)
    if catch_review is None:
        abort(404)
    storage.delete(catch_review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_places_id_reviews(place_id):
    """ POST method to add a review for place of id """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')
    catch_place = storage.get('Place', place_id)
    catch_user = storage.get('User', data['user_id'])
    if catch_place is None or catch_user is None:
        abort(404)
    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_reviews_id(review_id):
    """ PUT method to edit a review by review """
    catch_review = storage.get('Review', review_id)
    if catch_review is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'created_at', 'updated_at']:
            setattr(catch_review, key, value)
    storage.save()
    return jsonify(catch_review.to_dict()), 200
