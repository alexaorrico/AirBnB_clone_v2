#!/usr/bin/python3
'''
Methods and routes for working with review data
'''
from models.place import Place
from models.user import User
from models.review import Review
from models import storage
from flask import abort
from flask import jsonify
from flask import request
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    '''
    gets all reviews
    '''
    all_reivews = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = storage.all('Place').values()
    for review in reviews:
        all_reivews.append(review.to_dict())
    return jsonify(all_reivews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def retreive_review(review_id):
    '''
    gets 1 review object
    '''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    '''
    Deletes a review object
    '''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return ({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def make_review(place_id):
    '''
    creates a review object
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_name = request.get_json()
    if review_name is None:
        abort(400, 'not a JSON')
    if 'user_id' not in review_name:
        abort(400, 'Missing user_id')
    if 'text' not in Review:
        abort(400, 'Missing text')
    review = Review(**review_name)
    review.place_id = place_id
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''
    updates a review object
    '''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review_name = request.get_json()
    if not request.get.json():
        abort(400, 'not a JSON')
    for key, value in review_name.items():
        if key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(review, key, value)
    storage.save()
    all_places = review.to_dict()
    return jsonify(all_places, 200)
