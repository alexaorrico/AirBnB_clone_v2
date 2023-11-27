#!/usr/bin/python3
""" tbc """
import json
from flask import Flask, request, jsonify, abort
from models.place import Place
from models.user import User
from models.review import Review
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """ tbc """
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)
    places_reviews = the_place.reviews
    reviews_list = []
    for item in places_reviews:
        reviews_list.append(item.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_one_review(review_id):
    """ tbc """
    the_review = storage.get(Review, review_id)
    if the_review is not None:
        return jsonify(the_review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_one_review(review_id):
    """ tbc """
    the_review = storage.get(Review, review_id)
    if the_review is not None:
        storage.delete(the_review)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ tbc """
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)
    content = request.headers.get('Content-type')
    if content != 'application/json':
        abort(400, description='Not a JSON')
    json_dict = request.json
    if 'user_id' not in json_dict:
        abort(400, description='Missing user_id')
    the_user = storage.get(User, json_dict['user_id'])
    if the_user is None:
        abort(404)
    if 'text' not in json_dict:
        abort(400, description='Missing text')
    new_review = Review()
    setattr(new_review, 'place_id', place_id)
    for item in json_dict:
        setattr(new_review, item, json_dict[item])
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review_attribute(review_id):
    """ tbc """
    the_review = storage.get(Review, review_id)
    if the_review is None:
        abort(404)
    content = request.headers.get('Content-type')
    if content != 'application/json':
        abort(400, description='Not a JSON')
    j = request.json
    for i in j:
        if j[i] != 'id' and j[i] != 'created_at' and j[i] != 'updated_at':
            setattr(the_review, i, j[i])
    storage.save()
    return jsonify(the_review.to_dict()), 200
