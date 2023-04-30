#!/usr/bin/python3
"""creates a new view for Reviews that handles all Rest Api actions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def handle_reviews(place_id=None, review_id=None):
    """Retrieves the list of all review objects by places"""
    if place_id:
        # uses the '/places/<place_id>/reviews routes
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        else:
            if request.method == 'GET':
                review_list = []
                for reviews in place.reviews:
                    review_list.append(reviews.to_dict())
                return jsonify(review_list)
            elif request.method == 'POST':
                data = request.get_json()
                if not data:
                    abort(400, 'Not a JSON')
                if not data.get('user_id'):
                    abort(400, 'Missing user_id')
                user_id = storage.get(User, data.get('user_id'))
                if not user_id:
                    abort(404)
                if not data.get('text'):
                    abort(400, 'Missing text')
                data["place_id"] = place_id
                new_obj = Review(**data)
                new_obj.save()
                return jsonify(new_obj.to_dict()), 201

    if review_id:
        # uses the '/reviews/<review_id>' route
        review = storage.get(Review, review_id)
        if not review:
            abort(404)
        else:
            if request.method == 'GET':
                return jsonify(review.to_dict())
            elif request.method == 'DELETE':
                storage.delete(review)
                storage.save()
                return jsonify({}), 200
            elif request.method == 'PUT':
                ignore_keys = ["id", "created_at", "updated_at", "user_id",
                               "place_id"]
                data = request.get_json()
                if not data:
                    abort(400, 'Not a JSON')
                for key, value in data.items():
                    if key in ignore_keys:
                        continue
                    setattr(review, key, value)
                review.save()
                return jsonify(review.to_dict()), 200
