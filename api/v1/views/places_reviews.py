#!/usr/bin/python3
'''
API for Review
'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
import models


@app_views.route('/places/<place_id>/reviews/', methods=['GET'])
@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def all_places_reviews(place_id):
    '''Returns all review object by palce_id in json format'''
    json_list = []
    try:
        review_list = storage.get('Place', place_id).reviews
        for review in review_list:
            json_list.append(review.to_dict())
        return jsonify(json_list)
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    '''Retrieves a review for a place'''
    try:
        review = storage.get('Review', review_id).to_dict()
        return jsonify(review)
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    '''Deletes a review object from storage'''
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


def attrib_update(obj, **args):
    '''Helper function to update objects attributes to correct types'''
    for key, value in args.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            if hasattr(obj, key):
                if isinstance(value, str):
                    value = value.replace("_", " ")
            setattr(obj, key, value)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    '''Creates an instance of Review and save it to storage'''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    form = request.get_json(force=True)
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get('User', form['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request.json:
        return jsonify({"error": "Missing text"}), 400
    review_class = models.classes['Review']
    new_review = review_class(**form)
    setattr(new_review, 'place_id', place_id)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    '''Updates Review object attribute'''
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    form = request.get_json(force=True)
    attrib_update(review, **form)
    review.save()
    return jsonify(review.to_dict()), 200
