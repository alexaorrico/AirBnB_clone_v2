#!/usr/bin/python3
"""blueprint for the reviews"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from markupsafe import escape
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=["GET"])
def get_reviews_of_place(place_id):
    """this is the view for the /api/v1/places/[SLUG]/reviews
        endpoint"""
    res = storage.get(Place, escape(place_id))
    if not res:
        abort(404)
    res = storage.all(Review).values()
    res = [x.to_dict() for x in res if x.place_id == place_id]
    return jsonify(res)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=["GET"])
def get_review(review_id):
    """this is the view for the /api/v1/reviews/[SLUG]
        endpoint"""
    res = storage.get(Review, escape(review_id))
    if not res:
        abort(404)
    res = res.to_dict()
    return jsonify(res)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=["DELETE"])
def delete_review(review_id):
    """this is the view for the /api/v1/reviews/[SLUG]
        endpoint"""
    res = storage.get(Review, escape(review_id))
    if not res:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=["POST"])
def post_review_of_places(place_id):
    """this is the view for the /api/v1/places/[SLUG]/reviews
        endpoint"""
    res = storage.get(Place, escape(place_id))
    if not res:
        abort(404)
    try:
        body = request.get_json()
        if 'text' not in body.keys():
            return make_response(jsonify("Missing text"), 400)
        if 'user_id' not in body.keys():
            return make_response(jsonify("Missing user_id"), 400)
        new_review = Review(**body)
        new_review.place_id = place_id
        storage.new(new_review)
        storage.save()
        return make_response(jsonify(new_review.to_dict()), 201)
    except Exception as e:
        # print(f"exception is : {e}")
        return make_response(jsonify("Not a JSON"), 400)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=["PUT"])
def put_review(review_id):
    """this is the view for the /api/v1/reviews/[SLUG]
        endpoint"""
    res = storage.get(Review, escape(review_id))
    ignore_keys = ["id", "created_at", "updated_at"]
    if not res:
        abort(404)
    try:
        body = request.get_json()
        for key in body:
            if key not in ignore_keys:
                res.__dict__[key] = body[key]
        res.save()
        storage.save()
        return make_response(jsonify(res.to_dict()), 200)
    except Exception as e:
        return make_response(jsonify("Not a JSON"), 400)
