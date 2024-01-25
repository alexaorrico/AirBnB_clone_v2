#!/usr/bin/python3
"""Creates a new view for Place objects that
handles all default RESTFul API actions"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


# route to get all review objects
@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """returns all review objects"""
    place = storage.all(Place, place_id)
    if not place:
        abort(404)
    review_l = [review.to_dict() for review in place.reviews]
    return jsonify(review_l)


# route for getting a review obj based on its id
@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """returns review obj for the id input"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


# route for deleting a review obj using its id
@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """deletes a review obj"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


# route for creating a review obj
@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(city_id):
    """creates a review obj"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    """ transform the HTTP body request to a dictionary"""
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        abort(400, 'Missing user_id')
    if 'text' not in kwargs:
        abort(400, 'Missing text')

    user = storage.get(User, kwargs['user_id'])
    if not user:
        abort(404)

    kwargs['place_id'] = place_id
    review = Review(**kwargs)
    review.save()

    return jsonify(review.to_dict()), 201


# route for updating a review obj
@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """updates a review obj"""
    review = storage.get(Review, review_id)
    if review:
        if not request.get_json():
            abort(400, 'Not a JSON')

        """get JSON data from request"""
        new = request.get_json()
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        """update place obj with json data"""
        for key, value in new.items():
            if key not in ignore_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
