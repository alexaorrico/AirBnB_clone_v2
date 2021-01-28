#!/usr/bin/python3
"""handles review route requests"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=[
    'POST', 'GET'])
@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=[
    'PUT', 'GET', 'DELETE'])
def cities(place_id=None, review_id=None):
    """handles HTTP requests related to cities"""
    if place_id is not None:
        # /places/<place_id>/reviews GET method
        if request.method == 'GET':
            place = storage.all(Place)
            if place is not None:
                return jsonify([review for review in place.reviews])
            abort(404)

        # /places/<place_id>/reviews POST method
        if request.method == 'POST':
            new_json = request.get_json(silent=True)
            place = storage.get(Place, place_id)
            if place is None:
                abort(404)
            if new_json is None:
                abort(400, 'Not a JSON')
            if 'user_id' not in new_json:
                abort(400, 'Missing user_id')
            user = storage.get(User, new_json.get('user_id'))
            if user is None:
                abort(404)
            if 'text' not in new_json:
                abort(400, 'Missing text')
            new_review = Review(**new_json)
            new_review.place_id = place_id
            new_review.save()
            return jsonify(new_review.to_dict()), 201

    else:
        # /reviews/<review_id> GET method
        if request.method == 'GET':
            review = storage.get(Review, review_id)
            if review is not None:
                return jsonify(review.to_dict())
            abort(404)

        # /reviews/<review_id> DELETE method
        if request.method == 'DELETE':
            review = storage.get(Review, review_id)
            if review is not None:
                review.delete()
                storage.save()
                return jsonify({}), 200
            abort(404)

        # /reviews/<review_id> PUT method
        if request.method == 'PUT':
            review = storage.get(Review, review_id)
            if review is None:
                abort(404)
            new_json = request.get_json(silent=True)
            if new_json is None:
                abort(400, 'Not a JSON')
            for k, v in new_json.items():
                if k not in ['id', 'user_id', 'place_id',
                             'created_at', 'updated_at']:
                    setattr(review, k, v)
            review.save()
            return jsonify(review.to_dict()), 200
