#!/usr/bin/python3
<<<<<<< HEAD
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
=======
'''Contains the places_reviews view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def review(place_id):
    """Retrieves the list of all Review objects of a Place"""
    obj_place = storage.get(Place, place_id)
    if not obj_place:
        abort(404)
    return jsonify([obj.to_dict() for obj in obj_place.reviews])
>>>>>>> 7612747aa7ee76fbc856f9194eddf49ee9ebe535


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def single_review(review_id):
<<<<<<< HEAD
    '''Retrieve review object'''
=======
    """Retrieves a Review object"""
>>>>>>> 7612747aa7ee76fbc856f9194eddf49ee9ebe535
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


<<<<<<< HEAD
@app_views.route('/review/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    '''delete review object'''
    obj = storage.get(City, review_id)
=======
@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """Returns an empty dictionary with the status code 200"""
    obj = storage.get(Review, review_id)
>>>>>>> 7612747aa7ee76fbc856f9194eddf49ee9ebe535
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


<<<<<<< HEAD
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
=======
@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def push_review(place_id):
    """Returns the new Review with the status code 201"""
    obj_place = storage.get(Place, place_id)
    if not obj_place:
        abort(404)

    new_review = request.get_json()
    if not new_review:
        abort(400, "Not a JSON")
    if 'user_id' not in new_review:
        abort(400, "Missing user_id")
    user_id = new_review['user_id']
    obj_user = storage.get(User, user_id)
    if not obj_user:
        abort(404)
    if 'text' not in new_review:
        abort(400, "Missing text")

    obj = Review(**new_review)
    setattr(obj, 'place_id', place_id)
>>>>>>> 7612747aa7ee76fbc856f9194eddf49ee9ebe535
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


<<<<<<< HEAD
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
=======
@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Returns the Review object with the status code 200"""
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for k, v in req.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(obj, k, v)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)

>>>>>>> 7612747aa7ee76fbc856f9194eddf49ee9ebe535
