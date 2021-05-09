#!/usr/bin/python3
""" new view for Reviews """
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def getplacereviews(place_id):
    """ Gets reviews for a place """
    place = storage.get('Place', place_id)
    if place:
        reviews = []
        for review in place.reviews:
            reviews.append(review.to_dict())
        return (jsonify(reviews), 200)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def getreview(review_id):
    """ returns review using an ID """
    review = storage.get('Review', review_id)
    if review:
        return (jsonify(review.to_dict()), 200)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def deletereview(review_id):
    """ DELETE review with ID """
    review = storage.get('Review', review_id)
    if review:
        review.delete()
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/reviews/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def createreview(place_id):
    """ Create review for place ID """
    review_dict = request.get_json()
    place = storage.get('Place', place_id)
    if not review_dict:
        return(jsonify({"Error": "Not a JSON"}), 400)
    elif 'text' not in review_dict:
        return (jsonify({"error": "Missing text"}))
    elif 'user_id' not in review_dict:
        return (jsonify({"error": "Missing user_id"}), 400)
    elif storage.get('User', request.get_json()['user_id']) and place:
        review = Review(**review_dict)
        review.place_id = place_id
        review.save()
        return (jsonify(review.to_dict()), 201)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def updatereview(review_id):
    """ update review for review ID """
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    review_dict = request.get_json()
    review = storage.get('Review', review_id)
    if not review_dict:
        return (jsonify({"error": "Not a JSON"}), 400)
