#!/usr/bin/python3
"""This is the flask file for place reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def show_place_reviewe(place_id):
    """This method shows all reviews for a place
    """
    place = storage.get("Place", place_id)
    if place:
        return jsonify([r.to_dict() for r in place.reviews])
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['GET'])
def show_review(review_id):
    """ This method shows the review based on id
    """
    r = storage.get("Review", review_id)
    if r:
        return jsonify(r.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """This method deletes a review
    """
    r = storage.get("Review", review_id)
    if r:
        storage.delete(r)
        storage.save()
        return(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """This method creates a new review
    """
    vals = request.get_json(silent=True)
    p = storage.get("Place", place_id)
    if p is None:
        abort(404)
    if vals is None:
        abort(400, "Not a JSON")
    if "user_id" not in vals:
        abort(400, "Missing user_id")
    u_id = vals.get('user_id')
    u = storage.get("User", u_id)
    if u is None:
        abort(404)
    if "text" not in vals:
        abort(400, "Missing text")
    if "place_id" not in vals:
        vals['place_id'] = place_id
    r = Review()
    for k, v in vals.items():
        setattr(r, k, v)
    storage.new(r)
    storage.save()
    return (jsonify(r.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """This method updates the review
    """
    r = storage.get("Review", review_id)
    vals = request.get_json(silent=True)
    if vals is None:
        abort(400, "Not a JSON")
    if r is None:
        abort(404)
    for k, v in vals.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(r, k, v)
    storage.save()
    return(jsonify(r.to_dict()), 200)
