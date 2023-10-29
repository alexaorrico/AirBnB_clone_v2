#!/usr/bin/python3
''''''
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews_list = []
    for elem in place.reviews:
        reviews_list.append(elem.to_dict())
    return jsonify(reviews_list)

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    if not storage.get(Place, place_id):
        abort(404)
    query = request.get_json()
    if not query:
        abort(400, description='Not a JSON')
    if 'user_id' not in query:
        abort(400, description='Missing user_id')
    if not storage.get(User, query['user_id']):
        abort(404)
    if 'text' not in query:
        abort(400, description='Missing text')
    query['place_id'] = place_id
    new = Review(**query)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    return make_response(jsonify({}), 200)

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    if not storage.get(Review, review_id):
        abort(404)
    if request.content_type != 'application/json':
        abort(400, description='Not a JSON')
    review = storage.get(Review, review_id)
    query = request.get_json()
    ignore_list = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, val in query.items():
        if key not in ignore_list:
            setattr(review, key, val)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
        
