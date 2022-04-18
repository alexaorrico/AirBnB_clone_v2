#!/usr/bin/python3
""" reviews view module """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def reviews(place_id):
    """ Get reviews for a place """

    places = storage.all(Place)

    if Place.__name__ + '.' + place_id not in places.keys():
        abort(404)

    the_reviews = storage.all(Review)
    result = []
    for review in the_reviews.keys():
        try:
            if the_reviews[review].to_dict()['place_id'] == place_id:
                result.append(the_reviews[review].to_dict())
        except KeyError:
            abort(404)
    return jsonify(result), 200


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """ Get a particular review """
    try:
        the_review = storage.all(Review)[Review.__name__ + '.' + review_id]
        return jsonify(the_review.to_dict()), 200
    except KeyError:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def del_review(review_id):
    """ Delete a review """
    try:
        storage.all().pop(Review.__name__ + '.' + review_id)
        storage.save()
        return jsonify({}), 200
    except KeyError:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """ Create a new review """
    places = storage.all(Place)

    if Place.__name__ + '.' + place_id not in places.keys():
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()
    else:
        abort(400, 'Not a JSON')

    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    users = storage.all(User)
    if User.__name__ + '.' + data['user_id'] not in users.keys():
        abort(404)

    if 'text' not in data:
        abort(400, 'Missing text')

    data['place_id'] = place_id
    review = Review(**data)
    review.save()

    return jsonify(storage.get(Review, review.id).to_dict())


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def edit_review(review_id):
    """ Edit a given city, with a given data """
    the_reviews = storage.all(Review)

    if Review.__name__ + '.' + review_id not in the_reviews.keys():
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()
    else:
        abort(404, description='Not a JSON')

    review = Review(**data)
    review.save()

    return jsonify(storage.get(Review, review.id).to_dict())
