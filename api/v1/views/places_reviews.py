#!/usr/bin/python3
'''review view for API'''

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def places(place_id):
    '''list all review object of a given place'''
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404, 'Not found')
    if place_id:
        objs = storage.all('Reviews').values()
        obj_list = []
        for obj in objs:
            if (review_id == obj.place_id):
                obj_list.append(obj.to_dict())
        return jsonify(obj_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def single_review(review_id):
    '''Retrieve review object'''
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/review/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    '''delete review object'''
    obj = storage.get(City, review_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(review_id):
    '''return new review'''
    new_obj = request.get_json()
    if not new_obj:
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if 'user_id' not in new_obj:
        abort(400, "Missing user_id")
    if 'text' not in new_obj:
        abort(400, "Missing text")
    obj = Review(**new_obj)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    '''update review object'''
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id', 'user_id','place_id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
