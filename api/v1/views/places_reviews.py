#!/usr/bin/python3
"""views for reviews"""
from api.v1.views import app_views
from models import storage, review, place, user
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=["GET"])
def return_reviews(place_id):
    """return all city objects"""
    reviews = []
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    for rev in place_obj.reviews:
        reviews.append(rev.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=["GET"])
def return_review(review_id):
    """return single place object"""
    review_obj = storage.get('Review', review_id)
    if review_obj is None:
        abort(404)
    else:
        return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=["DELETE"])
def delete_review(review_id):
    """delete a review"""
    review_obj = storage.get('Review', review_id)
    if review_obj is None:
        abort(404)
    storage.delete(review_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/reviews', methods=["POST"])
def add_review(place_id):
    """add a review of place"""
    data = {}
    data = request.get_json(silent=True)
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    if data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")
    the_id = data['user_id']
    userid = storage.get("User", the_id).id
    if userid is None:
        abort(400, "Missing user_id")
    if data.get('text') is None:
        abort(400, "Missing text")
    new_review = review.Review(user_id=userid,
                               place_id=place_obj.id,
                               text=data.get('text'))
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["PUT"])
def update_review(review_id):
    """update a review"""
    data = {}
    review_obj = storage.get('Review', review_id)
    if review_obj is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review_obj, k, v)
    storage.save()
    return jsonify(review_obj.to_dict()), 200
