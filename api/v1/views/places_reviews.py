from flask import request, jsonify, abort
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_place_reviews(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews]), 200

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    review = Review.get(review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict()), 200

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    review = Review.get(review_id)
    if not review:
        abort(404)
    review.delete()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    place = Place.get(place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = User.get(data['user_id'])
    if not user:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    review = Review.get(review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
