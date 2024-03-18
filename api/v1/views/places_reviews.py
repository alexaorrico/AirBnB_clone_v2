#!/usr/bin/python3
""" State objects RESTFul API. """
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User

"""HTTP methods"""
G = 'GET'
P = 'POST'
D = 'DELETE'
Pu = 'PUT'


@app_views.route('/places/<place_id>/reviews', methods=[G],
                 strict_slashes=False)
def listing_reviews(place_id):
    """ List of reviews. """
    checking_reviews = storage.get(Place, place_id)
    if not checking_reviews:
        abort(404)
    list_of_places = [place.to_dict() for place in place_id.places]
    return jsonify(list_of_places)


@app_views.route('/reviews/<review_id>', methods=[G],
                 strict_slashes=False)
def review_by_id(review_id):
    """ Getting a review based on ID. """
    reviews = storage.get(Review, review_id)
    if not reviews:
        abort(404)
    return jsonify(reviews.to_dict())


@app_views.route('/reviews/<review_id>', methods=[D],
                 strict_slashes=False)
def deleting_review(review_id):
    """ Deleting Review based on ID. """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


app_views.route('/states/<state_id>/cities', methods=[P],
                 strict_slashes=False)
def creating_review(place_id):
    """ Creating a Review. """
    place = storage.get(Place, place_id)
    if not place:
        abort(404, 'Place not found')
    review_data = request.get_json(silent=True)
    if review_data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in review_data:
        abort(400, 'Missing user_id')
    user = storage.get(User, review_data['user_id'])
    if not user:
        abort(404, 'User not found')
    if 'text' not in review_data:
        abort(400, 'Missing text')
    new_review = Review(place_id=place_id,
                        user_id=review_data['user_id'],
                        text=review_data['text'])
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=[Pu],
                 strict_slashes=False)
def update_review(review_id):
    """ Updating Review. """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review_data = request.get_json(silent=True)
    if review_data is None:
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in review_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
