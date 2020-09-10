#!/usr/bin/python3
""" Restful API for User objects. """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    """ Retrieves a list with all Review object of a Place. """
    place_obj = storage.get(Place, place_id)
    if place_obj:
        review_objs = storage.all(Review).values()
        list_review = []
        for review in review_objs:
            if review.place_id == place_id:
                list_review.append(review.to_dict())
        return jsonify(list_review)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Get current place linked with the review_id"""
    review_obj = storage.get(Review, review_id)
    if review_obj:
        return jsonify(review_obj.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete current review """
    review_obj = storage.get(Review, review_id)
    if review_obj:
        storage.delete(review_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def new_review(place_id):
    """ Retrieves a new created Review. """
    body_dic = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not body_dic:
        return jsonify({'error': 'Not a JSON'}), 400
    if "user_id" not in body_dic:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, body_dic.get("user_id", None))
    if not user:
        abort(404)
    if "text" not in body_dic:
        return jsonify({'error': 'Missing text'}), 400

    new_review = Review(**body_dic)
    setattr(new_review, "place_id", place_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a current review"""
    review_obj = storage.get(Review, review_id)
    if review_obj:
        body_dic = request.get_json()
        if not body_dic:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in body_dic.items():
            setattr(review_obj, key, value)
        review_obj.save()
        return jsonify(review_obj.to_dict()), 200
    else:
        abort(404)
