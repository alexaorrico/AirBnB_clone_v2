#!/usr/bin/python3
""" new view for State objects """
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from flask import make_response, jsonify
import requests
from flask import request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id=None):
    obj = storage.get(Place, place_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    reviews_objs = [review.to_dict() for review in storage.all(Review).values()
                    if review.place_id == place_id]
    return make_response(jsonify(reviews_objs), 200)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    obj = storage.get(Review, review_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        return make_response(jsonify(obj.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """ Method DELETE """
    obj = storage.get(Review, review_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id=None):
    data = request.get_json(silent=True, force=True)
    if data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'text' not in data:
            return make_response(jsonify({'error': 'Missing text'}), 400)
        if 'user_id' not in data:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
    obj = storage.get(Place, place_id)
    obj_2 = storage.get(User, data['user_id'])
    if obj is None or obj_2 is None or (obj is None and obj_2 is None):
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        objs = Place(**data)
        objs.place_id = place_id
        objs.save()
    return make_response(jsonify(objs.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id=None):
    if review_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        obj = storage.get(Review, review_id)
        if obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            data = request.get_json(silent=True, force=True)
            if data is None:
                return make_response(jsonify({'error': 'Not a JSON'}), 400)
            [setattr(obj, key, value) for key, value in data.items()
             if key != (
                'id', 'user_id', 'created_at', 'place_id',
                'updated_at', 'state_id'
                )]
            obj.save()
            return make_response(jsonify(obj.to_dict()), 200)
