#!/usr/bin/python3
""" prepares data for easier viewing """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import OperationalError


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_all_places(place_id):
    """ Returns all the places in json """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    revs = storage.all('Review').values()
    return jsonify([rev.to_dict() for rev in revs if rev.place_id == place_id])


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_place(place_id=""):
    """ makes a new review """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    if request.mimetype != 'application/json':
        return jsonify(error="Not a JSON"), 400
    try:
        review_json = request.get_json()
    except BadRequest:
        return jsonify(error="Not a JSON"), 400
    if 'name' not in review_json:
        return jsonify(error="Missing name"), 400
    if 'user_id' not in review_json:
        return jsonify(error="Missing user_id"), 400
    if not storage.get('User', review_json['user_id']):
        abort(404)
    review = Review(**review_json)
    setattr(review, 'place_id', place.id)
    try:
        review.save()
    except OperationalError:
        return jsonify(error="Missing name"), 400
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_one_place(review_id=""):
    """ Returns specified review obj in json """
    if review_id:
        review = storage.get('review', review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def del_review(review_id=""):
    """ deletes the specified review """
    if review_id:
        review = storage.get('Review', review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id=""):
    """ updates an review """
    if review_id:
        review = storage.get('Review', review_id)
    if not review:
        abort(404)
    if request.mimetype != 'application/json':
        return jsonify(error="Not a JSON"), 400
    try:
        review_json = request.get_json()
    except BadRequest:
        return jsonify(error="Not a JSON"), 400
    """ remove the unwanted params """
    if review_json.get('id'):
        review_json.pop('id')
    if review_json.get('user_id'):
        review_json.pop('user_id')
    if review_json.get('place_id'):
        review_json.pop('place_id')
    if review_json.get('created_at'):
        review_json.pop('created_at')
    if review_json.get('updated_at'):
        review_json.pop('updated_at')
    if review_json.get('__class__'):
        review_json.pop('__class__')
    for k, v in review_json.items():
        setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict())
