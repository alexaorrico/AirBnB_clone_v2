#!/usr/bin/python3
"""New view for City object that handles all default Restfullapi actions"""
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def review_objs(place_id=None):
    """Return all Place objects"""
    place_objs = storage.get(Place, place_id)
    if place_objs:
        return jsonify([obj.to_dict() for obj in place_objs.reviews])
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_by_id(review_id=None):
    """Return a review by its id"""
    review_obj = storage.get(Review, review_id)
    if review_obj:
        return jsonify(review_obj.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """Deletes a review object"""
    review_objs = storage.get(Review, review_id)
    if review_objs:
        storage.delete(review_objs)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id=None):
    """Create place object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'text' not in request.get_json():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    dict_body = request.get_json()
    place_objs = storage.get(Place, place_id)
    user_objs = storage.get(User, dict_body["user_id"])
    if place_objs and user_objs:
        new_review = Review(**dict_body)
        new_review.place_id = place_objs.id
        storage.new(new_review)
        storage.save()
        return make_response(jsonify(new_review.to_dict()), 201)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def review_put(review_id=None):
    """Update review object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    dict_body = request.get_json()
    review_obj = storage.get(Review, review_id)
    if review_obj:
        for key, value in dict_body.items():
            if key != "id" and key != "created_at" and key != "updated_at"\
                    and key != "user_id" and key != "city_id":
                setattr(review_obj, key, value)
        storage.save()
        return make_response(jsonify(review_obj.to_dict()), 200)
    else:
        return abort(404)
