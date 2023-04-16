#!/usr/bin/python3
"""First route to display a json object"""
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, request
from models import storage
from api.v1.views import app_views


@app_views.route('/reviews/', methods=['GET', 'POST'],
                 defaults={'review_id': None})
@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'])
def reviews_views(review_id=None):
    if review_id is not None:
        my_review = storage.get(Review, review_id)
        if my_review is None:
            return jsonify(error='Review not found'), 404
        if request.method == 'GET':
            return jsonify(my_review.to_dict())
        if request.method == 'DELETE':
            storage.delete(my_review)
            storage.save()
            return {}, 200
        if request.method == 'PUT':
            update_values = request.get_json()
            if type(update_values) is not dict:
                return jsonify(error='Not a JSON'), 400
            for key, val in update_values.items():
                ls = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
                if key not in ls:
                    setattr(my_review, key, val)
                storage.save()
                return jsonify(my_review.to_dict())
    else:
        if request.method == 'GET':
            review_list = []
            for review in storage.all(Review).values():
                review_list.append(review.to_dict())
            return jsonify(review_list)
        # if request.method == 'POST':
        #     new_object = request.get_json()
        #     if type(new_object) is not dict:
        #         return jsonify(error='Not a JSON'), 400
        #     if 'user_id' not in new_object.keys():
        #         return jsonify(error='Missing user_id'), 400
        #     if 'text' not in new_object.keys():
        #         return jsonify(error='Missing text'), 400
        #     new_review = Review(**new_object)
        #     storage.new(new_review)
        #     storage.save()
        #     return jsonify(new_review), 201


@app_views.route('/places/<place_id>/reviews/', methods=['GET', 'POST'])
def review_by_place(place_id):
    """ review by place view model"""
    place = storage.get(Place, place_id)
    reviews = storage.all(Review)
    if place is None:
        return jsonify(error='No place found'), 404
    if request.method == "GET":
        new_review_list = []
        for review in place.reviews:
            new_review_list.append(review.to_dict())
        return jsonify(new_review_list), 200
    elif request.method == 'POST':
        update_values = request.get_json()
        if type(update_values) is not dict:
            return jsonify(error='Not a JSON'), 400
        if 'user_id' not in update_values.keys():
            return jsonify(error="Missing user_id"), 400
        if 'text' not in update_values.keys():
            return jsonify(error='Missing text'), 400
        user = storage.get(User, update_values['user_id'])
        if user is None:
            return jsonify(error="User not found"), 404
        new_review = Review(text=update_values['text'], user_id=user.id)
        return jsonify(new_review.to_dict()), 201
