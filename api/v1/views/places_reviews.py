#!/usr/bin/python3
""" Place Reviews Module """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.review import Review
from models import storage
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get(place_id):
    """ Returns a list of Reviews objects """
    place_obj = storage.get(Place, place_id)
    if place_obj:
        all_reviews = storage.all(Review)
        reviews = []
        for obj in all_reviews.values():
            if obj.place_id == place_id:
                reviews.append(obj.to_dict())
        return make_response(jsonify(reviews), 200)
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def one_review(review_id):
    """ Returns one review object """
    obj = storage.get(Review, review_id)
    if obj:
        return make_response(jsonify(obj.to_dict()), 200)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review obj if it exists """
    obj = storage.get(Review, review_id)
    if obj:
        obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def createReview(place_id):
    """ Creates a new Review object using a place_id """
    place_obj = storage.get(Place, place_id)
    if place_obj:
        if request.is_json is True:
            data = request.get_json()
            if "text" not in data:
                abort(400, "Missing text")
            if "user_id" in data:
                user_obj = storage.get(User, data["user_id"])
                if user_obj:
                    data["place_id"] = place_id
                    new_review = Review(**data)
                    storage.new(new_review)
                    storage.save()
                    return make_response(jsonify(new_review.to_dict()), 201)
                abort(404)
            abort(400, "Missing user_id")
        abort(400, "Not a JSON")
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update(review_id):
    """ Updates a review object """
    if request.is_json is True:
        data = request.get_json()
        obj = storage.get(Review, review_id)
        if obj:
            for key, value in data.items():
                if key not in ["id", "user_id", "place_id", "created_at",
                               "updated_at"]:
                    setattr(obj, key, value)
            obj.save()
            return make_response(jsonify(obj.to_dict()), 200)
        abort(404)
    abort(400, "Not a JSON")
