#!/usr/bin/python3
"""
Flask route that returns json status response on Reviews Objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def list_or_create_reviews(place_id):
    """
    get or add new review to a place given its ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        reviews = storage.all(Review)
        return jsonify([review.to_dict() for review in reviews.values(
        ) if review.to_dict().get("place_id") == place_id])
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if data.get("user_id") is None:
            abort(400, "Missing user_id")
        user = storage.get(User, data.get("user_id"))
        if user is None:
            abort(404)
        if data.get("text") is None:
            abort(400, "Missing text")
        data["place_id"] = place_id
        new_review = Review(**data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_or_delete_or_update_review(review_id):
    """
    get, add or update reviews given review_ID
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(
            review.to_dict()
        )
    if request.method == 'DELETE':
        review.delete()
        del review
        return jsonify({}), 200
    if request.method == 'PUT':
        update = request.get_json()
        if update is None:
            abort(400, 'Not a JSON')
        for key, val in update.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(review, key, val)
        review.save()
        return jsonify(review.to_dict()), 200
