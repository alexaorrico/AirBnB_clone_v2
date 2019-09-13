#!/usr/bin/python3
''' a new view for City objects that handles all default RestFul API '''
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews_of_place(place_id=None):
    ''' retrieves a list of all review objects of a given place '''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    reviews = storage.all('Review')
    reviews_list = []
    for val in reviews.values():
        if val.place_id == place_id:
            reviews_list.append(val.to_dict())

    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    ''' returns an individual review object given a review id '''
    obj = storage.get('Review', review_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    ''' deletes an individual review '''
    obj = storage.get('Review', review_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404)

    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"],
                 strict_slashes=False)
def create_review(place_id=None):
    ''' create a review '''
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
#    elif 'place_id' not in args:
#        return jsonify({"error": "Missing place_id"}), 400
    if 'user_id' not in args:
        return jsonify({"error": "Missing user_id"}), 400
    elif 'text' not in args:
        return jsonify({"error": "Missing text"}), 400

    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    user_id = args['user_id']
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    args['place_id'] = place_id
    obj = Review(**args)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201

"""
@app_views.route("/users/", methods=["POST"], strict_slashes=False)
def create_user():
    ''' create a user if doesn't already exist '''
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'email' not in args:
        return jsonify({"error": "Missing email"}), 400
    elif 'password' not in args:
        return jsonify({"error": "Missing password"}), 400
    obj = User(**args)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201
"""


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id=None):
    ''' updates an individual review '''
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400

    obj = storage.get('Review', review_id)
    if obj is None:
        ''' if no review obj with that id '''
        abort(404)

    for k, v in args.items():
        if k not in ["id", "place_id", "user_id", "updated_at", "created_at"]:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
