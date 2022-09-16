#!/usr/bin/python3
"""view cities object"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def reviews_by_places(place_id):
    """return list of all object reviews"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    reviews = list()
    list_review = storage.all('Review')
    for value in list_review.values():
        if place_id == value.place_id:
            reviews.append(value.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def review_by_id(review_id):
    """Get review by ID"""
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<reviews_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """Deletes an specific review"""
    ret = storage.get('Review', review_id)
    if ret:
        storage.delete(ret)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """Create a new review"""
    from models.review import Review
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    content = request.get_json(force=True, silent=True)
    if not content:
        abort(400, "Not a JSON")
    if "user_id" not in content.keys():
        abort(400, "Missing user_id")
    if "text" not in content.keys():
        abort(400, "Missing text")

    user = storage.get('User', content["user_id"])
    if not user:
        abort(404)
    text_review = content.get('text')
    id = content.get('user_id')

    new_instance = Review(text=text_review, user_id=id)
    return jsonify(new_instance.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """Update a review by a given ID"""
    new_review = storage.get('Review', review_id)
    if not new_review:
        abort(404)

    content = request.get_json(force=True, silent=True)
    if not content:
        abort(400, "Not a JSON")

    to_ignore = ['id', 'user_id', 'place_id', 'created_at', 'update_at']
    for key, value in content.items():
        if key in to_ignore:
            continue
        else:
            setattr(new_review, key, value)
    storage.save()
    return jsonify(new_review.to_dict()), 200
