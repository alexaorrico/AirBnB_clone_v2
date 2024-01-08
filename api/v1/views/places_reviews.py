#!/usr/bin/python3
"""Place-reviewes view"""
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all reviews objects"""
    from models import storage
    from models.place import Place
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object"""
    from models import storage
    from models.review import Review
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object"""
    from models import storage
    from models.review import Review
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Creates a place"""
    from models import storage
    from models.user import User
    from models.place import Place
    from models.review import Review
    from flask import request

    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    user_id = request.get_json()['user_id']
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    if 'text' not in request.get_json():
        return jsonify({"error": "Missing text"}), 400

    review = Review(**request.get_json())
    review.place_id = place_id
    review.user_id = user_id
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Updates a review object"""
    from models import storage
    from models.review import Review
    from flask import request
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id' 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
