#!/usr/bin/python3
"""
Places_reviews View
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """Gets all Reviews by using Place ID"""
    fetched_place = storage.get("Place", str(place_id))
    if fetched_place is None:
        abort(404)

    reviews_list = [review.to_dict() for review in fetched_place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Gets Review using an ID"""
    fetched_review = storage.get('Review', str(review_id))
    if fetched_review is None:
        abort(404)
    return jsonify(fetched_review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review based on the ID"""
    fetched_review = storage.get("Review", str(review_id))
    if fetched_review is None:
        abort(404)
    storage.delete(fetched_review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a review using place ID"""
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')

    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)

    user_id = review_json.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")

    user = storage.get("User", str(user_id))
    if user is None:
        abort(404)

    if "text" not in review_json:
        abort(400, 'Missing text')

    review_json["place_id"] = place_id

    new_review = Review(**review_json)
    new_review.save()
    resp = jsonify(new_review.to_dict())
    resp.status_code = 201

    return resp


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review"""
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')

    fetched_obj = storage.get("Review", str(review_id))
    if fetched_obj is None:
        abort(404)

    for k, val in review_json.items():
        if k not in ["id", "created_at", "updated_at", "user_id", "place_id"]:
            setattr(fetched_obj, k, val)

    fetched_obj.save()
    return jsonify(fetched_obj.to_dict()), 200
