#!/usr/bin/python3
""" handles all default RESTFul API actions for Place """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_review(place_id):
    """
        retrieves list of all Review of a specific Place
    """
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    else:
        review_list = []
        for review in places.reviews:
            review_list.append(review.to_dict())
    return (jsonify(review_list))


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def review_by_id(review_id):
    """
        retrieves review from a specific Place
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        review_dict = review.to_dict()
        return (jsonify(review_dict))


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
        delete specific review with given id
    """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
        create Review
    """
    # get the linked Place
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    #  transform the HTTP body request to a dictionary
    json_data = request.get_json()

    if not json_data:
        return (jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in json_data:
        return (jsonify({"error": "Missing user_id"}), 400)
    if 'text' not in json_data:
        return (jsonify({"error": "Missing text"}), 400)
    json_data['place_id'] = place_id
    # get linked user if exist
    user = storage.get(User, json_data['user_id'])
    if not user:
        abort(404)
    # State(**kwargs)
    newreview = Review(**json_data)
    newreview.save()
    # transform object in valid json
    newreview_dict = newreview.to_dict()
    return (jsonify(newreview_dict), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
        update Review
    """
    #  transform the HTTP body request to a dictionary
    json_data = request.get_json()
    if not json_data:
        return (jsonify({"error": "Not a JSON"}), 400)

    # get given review
    given_review = storage.get(Review, review_id)
    # if no review with right id
    if given_review is None:
        abort(404)

    # replace
    for key, value in json_data.items():
        # update item except this 3
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(given_review, key, value)

    storage.save()
    # transform object in valid json
    newreview_dict = given_review.to_dict()
    return (jsonify(newreview_dict), 200)
