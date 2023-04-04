#!/usr/bin/python3
"""routes /reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models.place import Place
from models.review import Review
from models import storage


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_from_places(place_id):
    """Method that retrieve a list of all reviews by places"""
    place = storage.get(Place, place_id)
    if (place is None):
        abort(404)

    reviews = place.reviews
    if (reviews is None):
        abort(404)

    res = [review.to_dict() for review in reviews]

    return (jsonify(res))


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_id(review_id):
    """Method that retrieve a list of all reviews by id"""
    review = storage.get(Review, review_id)
    if (review is None):
        abort(404)

    res = review.to_dict()
    return (jsonify(res))


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Method that delete a review by id"""
    review = storage.get(Review, review_id)
    if (review is None):
        abort(404)

    review.delete()
    storage.save()

    return (jsonify({}), 200)


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Method that post a new review"""
    if (not storage.get(Place, place_id)):
        abort(404)

    new_data = request.get_json(silent=True)

    if (type(new_data) is dict):
        new_review = Review(**new_data)
        setattr(new_review, "place_id", place_id)

        user = new_review.to_dict().get('user_id', None)
        if (not user):
            return jsonify({'message': 'Missing user_id'}), 400
        if (not storage.get(User, user)):
            abort(404)

        if (not new_review.to_dict().get('text', None)):
            return jsonify({'message': 'Missing text'}), 400

        new_review.save()
        return (jsonify(new_review.to_dict()), 201)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Method to update/put a review by id"""
    find_review = storage.get(Review, review_id)
    if (find_review is None):
        abort(404)

    update_review = request.get_json(silent=True)
    if (type(update_review) is dict):
        update_review.pop('id', None)
        update_review.pop('user_id', None)
        update_review.pop('place_id', None)
        update_review.pop('created_at', None)
        update_review.pop('updated_at', None)

        for key, value in update_review.items():
            setattr(find_review, key, value)
        find_review.save()
        return (jsonify(find_review.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)