#!/usr/bin/python3
'''Review routes'''
from flask import make_response, abort, request
from models import storage
from models.review import Review
from models.place import Place
from api.v1.views import app_views


@app_views.get('places/<place_id>/reviews')
def getAllReviewsByPlace(place_id):
    '''Retrieves the list of all Review objects of a Place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return make_response(reviews)


@app_views.post('places/<place_id>/reviews')
def createReview(place_id):
    '''Creates a review'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if not data.get('user_id'):
        abort(400, 'Missing user_id')
    if not data.get('text'):
        abort(400, 'Missing text')
    review = Review(**data, place_id=place_id)
    review.save()
    return make_response(review.to_dict(), 201)


@app_views.delete('reviews/<review_id>')
def deleteReview(review_id):
    '''Deletes a review'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response({})


@app_views.get('reviews/<review_id>')
def getReview(review_id):
    '''Gets a review'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return make_response(review.to_dict())


@app_views.put('reviews/<review_id>')
def updateReview(review_id):
    '''Updates a review'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    ignored = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignored:
            if k in review.__dict__:
                setattr(review, k, v)
    review.save()
    return make_response(review.to_dict())
