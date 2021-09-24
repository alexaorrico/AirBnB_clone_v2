#!/usr/bin/python3
""""""

from api.v1.views import app_views
from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


app = Flask(__name__)

@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def ret_all_bystate(place_id):
    """retrieve all by state_id"""
    reviews = []
    all = storage.get(Place, place_id)
    if all is not None:
        rev = all.reviews
        for x in rev:
            data = storage.get(Review, x.id)
            reviews.append(data.to_dict())
        return jsonify(reviews)
    else:
        abort(404)


@app_views.route('reviews/<review_id>', methods=['GET'], strict_slashes=False)
def ret_all_v(review_id):
    """retrieve all"""
    all = storage.get(Review, review_id)
    if all is not None:
        return jsonify(all.to_dict())
    else:
        abort(404)


@app_views.route('reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def deleterev_by_id(review_id):
    """deleteby review by id"""
    all = storage.get(Review, review_id)
    if all is not None:
        storage.delete(all)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """post review"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    all = storage.get(Place, place_id)
    if all is None:
        abort(404)
    if "text" not in request.get_json():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    if "user_id" not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", request.get_json()['user_id'])
    if user is None:
        abort(404)
    else:
        data = request.get_json()
        data['place_id'] = place_id
        ct = Review(**data)
        ct.save()
        return make_response(jsonify(ct.to_dict()), 201)


@app_views.route('reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """update review"""
    ignored = ['id', 'user_id', 'city_id', 'created_at',
               'updated_at']
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    for key, value in data.items():
        if key not in ignored:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
