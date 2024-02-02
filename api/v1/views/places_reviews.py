#!/usr/bin/python3
'''View to handle the RESTful API actions for 'User' objects'''
from flask import jsonify, request, abort

from api.v1.views import app_views
from models.user import User
from models.place import Place
from models.review import Review
from models import storage


@app_views.route('/places/<string:place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def reviews(place_id):
    '''Handles "/places/<place_id>/reviews" route'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    if request.method == 'POST':
        data = request.get_json()
        if data is None or type(data) is not dict:
            return 'Not a JSON', 400

        user_id = data.get('user_id')
        if user_id is None:
            return 'Missing user_id', 400
        if storage.get(User, user_id) is None:
            abort(404)

        text = data.get('text')
        if text is None:
            return 'Missing text', 400

        data['place_id'] = place_id
        review = Review(**data)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def review_actions(review_id):
    '''Handles actions for "/reviews/<review_id>" route'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None or type(data) is not dict:
            return 'Not a JSON', 400
        for attr, val in data.items():
            if attr not in ['id', 'user_id', 'place_id', 'created_at',
                            'updated_at']:
                setattr(review, attr, val)
        review.save()
        return jsonify(review.to_dict()), 200
