#!/usr/bin/python3
"""
New view for Review object that handles all default RestFul API actions
"""
from models.place import Place
from models.review import Review
from models import storage
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views


@app_views.route('/reviews', strict_slashes=False, methods=['GET'])
def all_reviews():
    '''
    Retrieves the list of all Review objects.
    '''
    Reviews_List = []
    for value in storage.all('Review').values():
        Reviews_List.append(value.to_dict())
    return jsonify(Reviews_List)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def all_reviews_of_a_place(place_id):
    '''
    Retrieves the list of all Review objects of a Place
    '''
    Reviews_List = []
    Place_Storage = storage.get('Place', place_id)
    if not Place_Storage:
        abort(404)
    for place in storage.all('Review').values():
        Places_List.append(city.to_dict())
    return jsonify(Places_List)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def specific_review(review_id):
    """ Retrieves a Review object. """
    Review_Storage = storage.get("Review", review_id)
    if Review_Storage is None:
        abort(404)
    return jsonify(Review_Storage.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Deletes a Review object. """
    Review_Storage = storage.get('Review', review_id)
    if Review_Storage:
        storage.delete(Review_Storage)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_Review(place_id):
    """ Creates a Review. """
    dic = request.get_json()
    Place_Storage = storage.get('Place', place_id)
    User_Storage = storage.get('User', dic["user_id"])
    if not Place_Storage:
        abort(404)
    if not User_Storage:
        abort(404)
    if not dic:
        abort(400, {'Not a JSON'})
    if 'text' not in dic:
        abort(400, {'Missing text'})
    if 'user_id' not in dic:
        abort(400, {'Missing user_id'})
    dic["place_id"] = place_id
    new_review = Review(**dic)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def updates_review(review_id):
    """ Updates a Review object. """
    dic = request.get_json()
    selected_review = storage.get('Review', review_id)
    if not selected_review:
        abort(404)
    if not dic:
        abort(400, {'Not a JSON'})
    for key, value in dic.items():
        if key not in ['id', 'user_id', 'place_id',
                       'updated_at', 'created_at']:
            setattr(selected_review, key, value)
    storage.save()
    return jsonify(selected_review.to_dict()), 200
