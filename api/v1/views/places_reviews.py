#!/usr/bin/python3
"""
this module creates a new view for Review objects
that handles all default RESTFul API actions
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def getReviewsByPlace(place_id):
    """
    returns all reviews for a place
    """
    if 'Place.{}'.format(place_id) in storage.all():
        dict_reviews = storage.all(Review)
        reviews_by_place = [v.to_dict() for v in dict_reviews.
                            values() if v.place_id == place_id]
        return jsonify(reviews_by_place), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def getReviewBydId(review_id):
    """
    returns review by its id
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict()), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def deleteReview(review_id):
    """
    deletes a review
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def createReview(place_id):
    """
    create a review
    """
    if 'Place.{}'.format(place_id) in storage.all():
        if request.is_json:
            argsDict = request.args
            argsDict = request.get_json()
            if 'user_id' not in argsDict:
                return jsonify(message="Missing user_id"), 400
            if 'User.{}'.format(argsDict['user_id']) not in storage.all(User):
                abort(404)
            if 'text' not in argsDict:
                return jsonify(massage="Missing text"), 400
            user_id = argsDict['user_id']
            text = argsDict['text']
            newReview = Review(place_id=place_id, user_id=user_id, text=text)
            newReview.save()
            newReviewDict = storage.get(Review, newReview.id).to_dict()
            return jsonify(newReviewDict), 201
        else:
            return jsonify(message="Not a JSON"), 400
    else:
        abort(404)


@app_views.route('//reviews/<review_id>',
                 strict_slashes=False, methods=['PUT'])
def updateReview(review_id):
    """
    updates review
    """
    review = storage.get(Review, review_id)
    if review:
        forbidden_key = [
            'id',
            'user_id',
            'place_id',
            'created_at',
            'updated_at']
        if request.is_json:
            argsDict = request.args
            argsDict = request.get_json()
            for k, v in argsDict.items():
                if k not in forbidden_key:
                    setattr(review, k, v)
            review.save()
            return jsonify(review.to_dict()), 200
        else:
            return jsonify('Not a JSON'), 400
    else:
        abort(404)
