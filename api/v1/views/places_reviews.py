#!/usr/bin/python3
"""
module places_reviews.py
"""

from flask import abort, jsonify, request
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviewObjOfPlaces(place_id):
    """Retrieves the list of all Review objects of a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviewList = []
    """same as cities_list = [city.to_dict() for city in state.cities]"""
    for rev in place.reviews:
        reviewList.append(rev.to_dict())
    return jsonify(reviewList)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def reviewObj(review_id):
    """Retrieves a Review object."""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def reviewDeleteWithId(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def createReview(place_id):
    """Creates a Review: POST /api/v1/places/<place_id>/reviews"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    place = storage.get(Place, place_id)
    if place:
        newReviewData = request.get_json()

        if not newReviewData.get('user_id'):
            abort(400, description='Missing user_id')

        review_userId = newReviewData.get('user_id')
        user = storage.get(User, review_userId)
        if not user:
            abort(404)
        if not newReviewData.get('text'):
            abort(400, description='Missing text')

        newReviewData['place_id'] = city_id

        newReviewObj = Review(**newReviewData)
        storage.new(newReviewObj)
        storage.save()

        return jsonify(newReviewObj.to_dict()), 201
    else:
        abort(404)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def updateReview(review_id):
    """Updates a Review object"""
    reviewObj = storage.get(Review, review_id)
    if reviewObj:
        update = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        ignoredKeys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for k, v in update.items():
            if k not in ignoredKeys:
                setattr(reviewObj, k, v)

        storage.save()
        return jsonify(reviewObj.to_dict()), 200
    else:
        abort(404)
