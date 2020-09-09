#!/usr/bin/python3
""" Flask routes for `Review` object related URI subpaths using the
`app_views` Blueprint.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def GET_all_Review(place_id):
    """ Returns JSON list of all `Review` instances associated
    with a given `Place` instance in storage

    Args:
        place_id (str): UUID of `Place` instance in storage

    Return:
        JSON list of all `Review` instances for a given `Place` instance
    """
    place = storage.get(Place, place_id)

    if place:
        review_list = []
        for review in place.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def GET_Review(review_id):
    """ Returns `Review` instance in storage by id in URI subpath

    Args:
        review_id (str): UUID of `Review` instance in storage

    Return:
        `Review` instance with corresponding uuid, or 404 response
    on error
    """
    review = storage.get(Review, review_id)

    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def DELETE_Review(review_id):
    """ Deletes `Review` instance in storage by id in URI subpath

    Args:
        review_id (str): UUID of `Review` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
    """
    review = storage.get(Review, review_id)

    if review:
        storage.delete(review)
        storage.save()
        return ({})
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def POST_Review(place_id):
    """ Creates new `Review` instance in storage for `Place` instance
    corresponding to given UUID

    Args:
        place_id (str): UUID of `Place` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
    """
    place = storage.get(Place, place_id)

    if place:
        req_dict = request.get_json()
        if not req_dict:
            return (jsonify({'error': 'Not a JSON'}), 400)
        elif 'text' not in req_dict:
            return (jsonify({'error': 'Missing text'}), 400)
        elif 'user_id' not in req_dict:
            return (jsonify({'error': 'Missing user_id'}), 400)
        text = req_dict.get('text')
        user_id = req_dict.get('user_id')
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        new_Review = Review(text=text, place_id=place_id, user_id=user_id)
        new_Review.save()

        return (jsonify(new_Review.to_dict()), 201)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def PUT_Review(review_id):
    """ Updates `Review` instance in storage by id in URI subpath, with
    kwargs from HTTP body request JSON dict

    Args:
        review_id: uuid of `Review` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
    """
    review = storage.get(Review, review_id)

    if review:
        req_dict = request.get_json()
        if not req_dict:
            return (jsonify({'error': 'Not a JSON'}), 400)
        for key, value in req_dict.items():
            if key not in ['id', 'created_at', 'updated_at',
                           'user_id', 'place_id']:
                setattr(review, key, value)
        storage.save()
        return (jsonify(review.to_dict()))
    else:
        abort(404)
