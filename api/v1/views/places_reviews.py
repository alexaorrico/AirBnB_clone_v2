#!/usr/bin/python3
"""This module defines a view for the link between Place and Review objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def place_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage_t == 'db':
        reviews = place.reviews
    else:
        reviews = [storage.get(Review, review_id)
                   for review_id in place.review_ids]
    return jsonify([review.to_dict() for review in reviews])


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def place_review(place_id, amenity_id):
    """Deletes or links an Review object to a Place"""
    place = storage.get(Place, place_id)
    review = storage.get(Review, review_id)
    if place is None or review is None:
        abort(404)
    if request.method == 'DELETE':
        if storage_t == 'db':
            if review not in place.reviews:
                abort(404)
            place.reviews.remove(review)
        else:
            if review_id not in place.review_ids:
                abort(404)
            place.review_ids.remove(review_id)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'POST':
        if storage_t == 'db':
            if review in place.reviews:
                return jsonify(review.to_dict()), 200
            place.reviews.append(review)
        else:
            if review_id in place.review_ids:
                return jsonify(review.to_dict()), 200
            place.review_ids.append(review_id)
        storage.save()
        return jsonify(review.to_dict()), 201
