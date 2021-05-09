#!/usr/bin/python3
"""View configuration for Places-Review"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, place
from models.place import Place
from models.review import Review

@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Gets all reviwes depending of place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    res = []
    for i in city.reviews:
        res.append(i.to_dict())
    return jsonify(res)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def getplaces(review_id=None):
    """Gets a review according with the id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteplaces(review_id=None):
    """Deletes a review according with the id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        review.delete()
        storage.save()
        return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def jsonify_review_4(place_id):
    try:
        json_post = request.get_json()
        the_obj = storage.get(Place, place_id)
        if the_obj is None:
            abort(404)
        if not json_post:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'user_id' not in json_post:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        if 'text' not in json_post:
            return make_response(jsonify({'error': 'Missing text'}), 400)
        json_post['place_id'] = place_id
        new = Review(**json_post)
        new.save()
        return make_response(jsonify(new.to_dict()), 201)
    except:
        abort(404)
