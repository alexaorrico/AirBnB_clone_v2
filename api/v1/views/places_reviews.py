#!/usr/bin/python3
"""Renders json view for review objects
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=['GET'])
def reviews_of_place(place_id):
    """returns list of reviews of a place
    """
    place = storage.get("Place", place_id)
    if place:
        return jsonify([r.to_dict() for r in place.reviews])
    abort(404)


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """create a review for a place
    """
    from models.review import Review
    place = storage.get("Place", place_id)
    if place:
        body = request.get_json()
        if not body:
            return make_response('Not a JSON', 400)
        if not body.get('user_id'):
            return make_response('Missing user_id', 400)
        if not storage.get("User", body.get('user_id')):
            abort(404)
        if not body.get('text'):
            return make_response('Missing text', 400)
        review = Review(
                        user_id=body.get('user_id'),
                        place_id=place_id,
                        text=body.get('text')
                        )
        storage.new(review)
        storage.save()
        return make_response(jsonify(review.to_dict()), 201)
    abort(404)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """returns a review
    """
    review = storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """delete a review
    """
    review = storage.get("Review", review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=['PUT'])
def modify_review(review_id):
    """modify a review object
    """
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    review = storage.get("Review", review_id)
    if review:
        body = request.get_json()
        if not body:
            return make_response('Not a JSON', 400)
        for k, v in body.items():
            if k not in ignore:
                setattr(review, k, v)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
    abort(404)
