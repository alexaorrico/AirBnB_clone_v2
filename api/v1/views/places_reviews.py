#!/usr/bin/python3
"""
    This is the places reviews page handler for Flask.
"""
from api.v1.views.places import places_id
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request

from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<id>/reviews', methods=['GET', 'POST'])
def places_id_reviews(id):
    """
        Flask route at /places/<id>/reviews.
    """
    place = storage.get(Place, id)
    if (place):
        if request.method == 'POST':
            kwargs = request.get_json()
            if not kwargs:
                return {"error": "Not a JSON"}, 400
            if "user_id" not in kwargs:
                return {"error": "Missing user_id"}, 400

            user = storage.get(User, kwargs.get("user_id", None))
            if (user):
                if "text" not in kwargs:
                    return {"error": "Missing text"}, 400
                new_review = Review(place_id=id, **kwargs)
                new_review.save()
                return new_review.to_dict(), 201

        elif request.method == 'GET':
            return jsonify([r.to_dict() for r in place.reviews])
    abort(404)


@app_views.route('/reviews/<id>', methods=['GET', 'DELETE', 'PUT'])
def reviews_id(id):
    """
        Flask route at /reviews/<id>.
    """
    review = storage.get(Review, id)
    if (review):
        if request.method == 'DELETE':
            review.delete()
            storage.save()
            return {}, 200

        elif request.method == 'PUT':
            kwargs = request.get_json()
            if not kwargs:
                return {"error": "Not a JSON"}, 400
            for k, v in kwargs.items():
                if k not in ["id", "user_id", "place_id",
                             "created_at", "updated_at"]:
                    setattr(review, k, v)
            review.save()
        return review.to_dict()
    abort(404)
