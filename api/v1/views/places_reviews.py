#!/usr/bin/python3
"""Review view for the web service API"""
from flask import jsonify, abort, request
from api.v1.views import app_views  # Blueprint object
from models import storage
from models.place import Place
from models.user import User
from models.review import Review

# Route to get reviews


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """Return a JSON reponse of all review objects specified by place id
    """

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    # Get list of review objects dictionary by city_id
    review_objs = [review.to_dict() for review in storage.all(
        Review).values() if review.place_id == place_id]

    return jsonify(review_objs)

# Route to get a review object


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Return a JSON reponse of a review object specified by place id
    """

    # Get dictionary of review object by id
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


# Route to delete a review object


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review object specified by it id"""

    review = storage.get(Review, review_id)

    if not review:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
    return jsonify({}), 200

# Route to create a review object


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Create a new place object"""

    content = request.get_json()  # Content body
    if type(content) is not dict:
        abort(400, 'Not a Json')  # raise bad request error
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if 'user_id' not in content:
        abort(400, 'Missing user_id')  # raise bad request error
    if 'text' not in content:
        abort(400, 'Missing text')

    user = storage.get(User, content['user_id'])
    if not user:
        abort(404)
    review = Review(**content)
    review.save()

    return jsonify(review.to_dict()), 201

# Route to update a review object


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Update a review object specified by id"""

    review = storage.get(Review, review_id)  # Get review by id

    if not review:
        abort(404)  # raise not found error

    content = request.get_json()  # Content body
    if type(content) is not dict:
        abort(400, 'Not a Json')  # raise bad request error
    for k, v in content.items():
        if k not in ['id', 'created_at', 'updated_at', 'place_id', 'user_id']:
            setattr(review, k, v)  # Update review with new data
            review.save()

    return jsonify(review.to_dict()), 200
