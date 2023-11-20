#!/usr/bin/python3
"""Create a new view for Review objects that
handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """ Gets all Review objects of Place """
    all_review_list = []
    place_obj = storage.get(Place, place_id)
    if place_obj:
        for value in storage.all(Review).values():
            if value.place_id == place_id:
                all_review_list.append(value.to_dict())
        return jsonify(all_review_list)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Gets a Review object """
    review_obj = storage.get(Review, review_id)
    if review_obj:
        return jsonify(review_obj.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review_obj = storage.get(Review, review_id)
    if review_obj:
        storage.delete(review_obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ Creates a new Review object """
    json_body = request.get_json()
    place_obj = storage.get(Place, place_id)
    if place_obj:
        if json_body:
            if 'user_id' not in json_body:
                return make_response(jsonify({'error': 'Missing user_id'}),
                                     400)
            elif 'text' not in json_body:
                return make_response(jsonify({'error': 'Missing text'}), 400)
            else:
                if storage.get(User, json_body['user_id']):
                    json_body["place_id"] = place_id
                    new_review = Review(**json_body)
                    new_review.save()
                    return make_response(jsonify(new_review.to_dict()), 201)
                else:
                    abort(404)
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object"""
    json_body = request.get_json()
    review_obj = storage.get(Review, review_id)
    if json_body:
        if review_obj:
            for key, value in json_body.items():
                if key not in ['id', 'user_id', 'place_id',
                               'created_at', 'updated_at']:
                    setattr(review_obj, key, value)
            review_obj.save()
            return make_response(jsonify(review_obj.to_dict()), 200)
        else:
            abort(404)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
