#!/usr/bin/python3
""" Method HTTP for City """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """ Function that retrieves the list of all Reviews """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)

    all_reviews = []
    for review in place.reviews:
        all_reviews.append(review.to_dict())
    return jsonify(all_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Function that retrieves a Review """
    review = storage.get(Review, review_id)
    return abort(404) if review is None else jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Function that deletes a review """
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """ Function that create a Review """
    dico = request.get_json()

    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)

    if dico is None:
        abort(400, "Not a JSON")

    if dico.get("user_id") is None:
        abort(400, "Missing user_id")

    user_id = storage.get(User, dico['user_id'])
    if user_id is None:
        return abort(404)

    if dico.get("text") is None:
        abort(400, "Missing text")

    dico['place_id'] = place_id
    new_review = Review(**dico)
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """ Function that update a Review """
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)

    dico = request.get_json()

    if dico is None:
        abort(400, "Not a JSON")

    for k, value in dico.items():
        if k not in ['id', 'created_at', 'updated_at', 'user_id', 'place_id']:
            setattr(review, k, value)
    review.save()

    return jsonify(review.to_dict()), 200
