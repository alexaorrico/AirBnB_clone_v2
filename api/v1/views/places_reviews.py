#!/usr/bin/python3
""" Places reviews routes handler """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import place
from models import review
from models import user


def do_check_id(cls, review_id):
    """
        If the review_id is not linked to any Review object, raise a 404 error
    """
    try:
        get_review = storage.get(cls, review_id)
        get_review.to_dict()
    except Exception:
        abort(404)
    return get_review


def do_get_reviews(place_id, review_id):
    """
       Retrieves the list of all Review objects
       if review_id is not none get a Review object
    """
    if (review_id is not None):
        get_review = do_check_id(review.Review, review_id).to_dict()
        return jsonify(get_review)
    my_place = storage.get(place.Place, place_id)
    try:
        all_reviews = my_place.reviews
    except Exception:
        abort(404)
    reviews = []
    for c in all_reviews:
        reviews.append(c.to_dict())
    return jsonify(reviews)


def do_delete_review(review_id):
    """
        Deletes a Review object
        Return: an empty dictionary with the status code 200
    """
    get_review = do_check_id(review.Review, review_id)
    storage.delete(get_review)
    storage.save()
    response = {}
    return jsonify(response)


def do_create_review(request, place_id):
    """
        Creates a review object
        Return: new review object
    """
    do_check_id(place.Place, place_id)
    body_request = request.get_json(silent=True)
    if (body_request is None):
        abort(400, 'Not a JSON')
    try:
        user_id = body_request['user_id']
    except KeyError:
        abort(400, 'Missing user_id')
    do_check_id(user.User, user_id)
    try:
        review_text = body_request['text']
    except KeyError:
        abort(400, 'Missing text')
    new_review = review.Review(text=review_text,
                               place_id=place_id,
                               user_id=user_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict())


def do_update_review(review_id, request):
    """
        Updates a Review object
    """
    get_review = do_check_id(review.Review, review_id)
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    for k, v in body_request.items():
        if (k not in ('id', 'created_at', 'updated_at')):
            setattr(get_review, k, v)
    storage.save()
    return jsonify(get_review.to_dict())


@app_views.route('/places/<place_id>/reviews/', methods=['GET', 'POST'],
                 defaults={'review_id': None}, strict_slashes=False)
@app_views.route('/reviews/<review_id>', defaults={'place_id': None},
                 methods=['GET', 'DELETE', 'PUT'])
def reviews(place_id, review_id):
    """
        Handle reviews requests with needed functions
    """
    if (request.method == "GET"):
        return do_get_reviews(place_id, review_id)
    elif (request.method == "DELETE"):
        return do_delete_review(review_id)
    elif (request.method == "POST"):
        return do_create_review(request, place_id), 201
    elif (request.method == "PUT"):
        return do_update_review(review_id, request), 200
