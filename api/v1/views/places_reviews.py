#!/usr/bin/python3
""" Reviews view """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    """ Returns a list of all the reviews of a place """
    if not storage.get("Place", place_id):
        abort(404)

    reviews = []
    for review in storage.all("Review").values():
        if review.place_id == place_id:
            reviews.append(review.to_dict())

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review(review_id):
    """ Returns a particular review by id """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """ Deletes a particular review based on id """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def add_review(place_id):
    """ Create a new review """
    if not storage.get("Place", place_id):
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    user_id = request.get_json().get('user_id')
    if not user_id:
        abort(400, description="Missing user_id")

    if not storage.get("User", user_id):
        abort(404)

    if not request.get_json().get('text'):
        abort(400, description="Missing text")

    review = Review()
    review.text = request.get_json()['text']
    review.place_id = place_id
    review.user_id = user_id
    review.save()

    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a particular review """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for key, value in request.get_json().items():
        if key == "id" or key == "created_at" or key == "updated_at" \
           or key == "user_id" or key == "place_id":
            continue
        else:
            setattr(review, key, value)

    storage.save()

    return make_response(jsonify(review.to_dict()), 200)
