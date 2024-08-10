#!/usr/bin/python3
"""Place Reviews API"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<string:place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def get_place_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)

    if place is None:
        return jsonify({'error': 'Not found'}), 404
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews), 200


@app_views.route("/reviews/<string:review_id>", strict_slashes=False,
                 methods=['GET'])
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<string:review_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({'error': 'Not found'}), 404
    review.delete()
    return jsonify({}), 200


@app_views.route("/places/<string:place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'error': 'Not found'}), 404

    if request.is_json:
        data = request.get_json()
        user_id = data.get('user_id', None)
        text = data.get('text', None)
        if user_id is None or user_id == "":
            return jsonify({'error': 'Missing user_id'}), 400
        user = storage.get(User, user_id)
        if user is None:
            return jsonify({'error': 'Not found'}), 404

        if text is None or text == "":
            return jsonify({'error': 'Missing text'}), 400

        review = Review(place_id=place_id, user_id=user_id, text=text)
        review.save()
        return jsonify(review.to_dict()), 201
    return jsonify({'error': 'Not a JSON'}), 400


@app_views.route("/reviews/<string:review_id>", strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is not None:
        if request.is_json:
            data = request.get_json()
            data = {k: v for k, v in data.items() if k != 'id' and
                    k != 'created_at' and k != 'updated_at' and
                    k != 'user_id' and k != 'place_id'}
            for k, v in data.items():
                setattr(review, k, v)
            review.save()
            review = storage.get(Review, review_id)
            return jsonify(review.to_dict()), 200
        return jsonify({'error': 'Not a JSON'}), 400
    return jsonify({'error': 'Not found'}), 404
