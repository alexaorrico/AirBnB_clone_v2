"""Module providing API endpoints for Review resources."""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieve a list of reviews for a specific place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_list)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve information about a specific review."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a review by its ID."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new review for a specific place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        if 'user_id' not in data:
            return jsonify({"error": "Missing user_id"}), 400
        if 'text' not in data:
            return jsonify({"error": "Missing text"}), 400

        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)

        review = Review(**data)
        review.place_id = place_id
        storage.new(review)
        storage.save()

        return jsonify(review.to_dict()), 201
    else:
        return jsonify({"error": "Not a JSON"}), 400

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Update a review's information."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        keys_to_ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in keys_to_ignore:
                setattr(review, key, value)
        review.save()

        return jsonify(review.to_dict()), 200
    else:
        return jsonify({"error": "Not a JSON"}), 400
