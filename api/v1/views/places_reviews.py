#!/usr/bin/python3
"""Review views for API"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Return reviews list in format JSON"""
    reviews = storage.all(Review)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    lis_review = []
    for review in reviews.values():
        if place.id == reviews.place_id:
            lis_review.append(review.to_dict())
    return jsonify(lis_review)


@app_views.route("reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Return a specific reviews object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete review id"""
    reviews = storage.all()
    for review in reviews.values(Review):
        if review.id == review_id:
            storage.delete(review)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a review"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if "user_id" not in data:
        abort(400, 'Missing user_id')
    if "text" not in data:
        abort(400, 'Missing text')

    if not storage.get(Place, place_id):
        abort(404)
    if not storage.get(User, data["user_id"]):
        abort(404)

    new_review = Review(**data)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update given review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
