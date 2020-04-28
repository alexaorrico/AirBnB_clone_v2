#!/usr/bin/python3
""" Places reviews """
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def review_by_id(place_id):
    """ List al reviws in a place id """
    rev = []c
    place = storage.all('Review')
    if place:
        for key, value in place.items():
            if value.to_dict()['place_id'] == place_id:
                rev.append(value.to_dict())
        return jsonify(rev)
    else:
        abort(404)


@app_views.route("/review/<review_id>", method=['GET'], strict_slashes=False)
def review_object(review_id):
    """ Return the review id requested """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ delete a review object """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ create a new review object """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    kwargs = request.get_json()
    if "user_id" not in kwargs:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get("User", kwargs["user_id"])
    if user is None:
        abort(404)
    if "text" not in kwargs:
        return make_response(jsonify({"error": "Missing text"}), 400)
    kwargs['place_id'] = place_id
    review = Review(**kwargs)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """ update a review instance """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'place_id',
                        'created_at', 'updated_at']:
            setattr(review, attr, val)
            review.save()
            return jsonify(review.to_dict())


def item_locator(id, item):
    """ fin into items list """
    if item == 'User':
        users = storage.all('User').items()
        for key, value in users:
            if value.to_dict()['id'] == id:
                return True
        return False
    if item == 'Place':
        place = storage.all('Place').items()
        for key, value in place:
            if value.to_dict()['id'] == id:
                return True
        return False
