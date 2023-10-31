#!/usr/bin/python3
'''Places_reviews view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_reviews(place_id=None, review_id=None):
    '''The method handler for the reviews endpoint.
    '''
    handlers = {
        'GET': get_reviews,
        'DELETE': remove_review,
        'POST': add_review,
        'PUT': update_review
    }
    if request.method in handlers:
        return handlers[request.method](place_id, review_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_reviews(place_id=None, review_id=None):
    '''Gets the review with the given id or all reviews in
    the place with the given id.
    '''
    if place_id:
        v_place = storage.get(Place, place_id)
        if v_place:
            reviews = []
            for p_review in v_place.reviews:
                reviews.append(p_review.to_dict())
            return jsonify(reviews)
    elif review_id:
        p_review = storage.get(Review, review_id)
        if p_review:
            return jsonify(p_review.to_dict())
    raise NotFound()


def remove_review(place_id=None, review_id=None):
    '''Removes a review with the given id.
    '''
    p_review = storage.get(Review, review_id)
    if p_review:
        storage.delete(p_review)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_review(place_id=None, review_id=None):
    '''Adds a new review.
    '''
    v_place = storage.get(Place, place_id)
    if not v_place:
        raise NotFound()
    v_data = request.get_json()
    if type(v_data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'user_id' not in v_data:
        raise BadRequest(description='Missing user_id')
    v_user = storage.get(User, v_data['user_id'])
    if not v_user:
        raise NotFound()
    if 'text' not in v_data:
        raise BadRequest(description='Missing text')
    v_data['place_id'] = place_id
    new_review = Review(**v_data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


def update_review(place_id=None, review_id=None):
    '''Updates the review with the given id.
    '''
    xkeys = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    if review_id:
        p_review = storage.get(Review, review_id)
        if p_review:
            v_data = request.get_json()
            if type(v_data) is not dict:
                raise BadRequest(description='Not a JSON')
            for key, value in v_data.items():
                if key not in xkeys:
                    setattr(p_review, key, value)
            p_review.save()
            return jsonify(p_review.to_dict()), 200
    raise NotFound()
 
