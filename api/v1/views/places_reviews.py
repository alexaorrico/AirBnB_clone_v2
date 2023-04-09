#!/usr/bin/python3

from flask import abort, jsonify
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def review_list(place_id):
    """returns reviews for a place given"""

    from models import storage
    from models.place import Place
    from models.review import Review

    place_found = storage.get(Place, place_id)
    if place_found == None:
        abort(404)

    list_of_reviews = storage.all(Review)
    review_list = []

    for review in list_of_reviews:
        if review.place_id == place_id:
            review_list.append(review.to_dict())

    return jsonify(review_list)


@app_views.route('/review/<review_id>', methods=['GET'])
def review(review_id):
    """returns review of id given"""

    from models import storage
    from models.review import Review

    review_found = storage.get(Review, review_id)
    if review_found == None:
        abort(404)

    return jsonify(review_found.to_dict()), 201


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    """create a review and link to place"""
    from flask import request
    from models import storage
    from models.place import Place
    from models.user import User
    from models.review import Review

    http_request = request.get_json(silent=True)
    if http_request == None:
        return 'Not a JSON', 400
    elif 'text' not in http_request.keys():
        return 'Missing text', 400
    elif 'user_id' not in http_request.keys():
        return 'Missing user_id', 400

    if storage.get(User, http_request.user_id) == None or storage.get(Place, place_id) == None:
        abort(404)

    new_review = Review(**http_request)
    new_review.place_id = place_id
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """updates given review"""

    from flask import request
    from models import storage
    from models.review import Review

    found_review = storage.get(Review, review_id)

    if found_review == None:
        return '', 404

    http_request = request.get_json(silent=True)
    if http_request == None:
        return 'Not a JSON', 400

    for key, values in http_request.items():
        if key not in ['id', 'user_id', 'place_id' 'created_at', 'updated_at']:
            setattr(found_review, key, values)

    storage.save()
    return jsonify(found_review.to_dict()), 201


@app_views.route('/review/<review_id>', methods=['DELETE'])
def review_delete(review_id):
    """DELETE review if id is found"""

    from models import storage
    from models.review import Review

    review_found = storage.get(Review, review_id)
    if review_found == None:
        return '{}', 404

    storage.delete(review_found)
    storage.save()
    return jsonify({}), 200
