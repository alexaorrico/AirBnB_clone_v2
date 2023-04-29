#!/usr/bin/python3
"""A script that handles RESTFul API"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, CNC


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def place_review(place_id):
    """A route that fetches reviews of all placess
    and also create one.
    Return:
        for GET: retrieve listin json format
        for POST: create reviewwith status code
    """
    place = storage.get("Place", place_id)

    if request.method == 'GET':
        if place is None:
            abort(404, 'Not found')
        reviews = storage.all('Review')
        place_reviews = list(pr.to_json() for pr in reviews.values()
                             if pr.place_id == place_id)
        return jsonify(place_reviews)

    if request.method == 'POST':
        if place is None:
            abort(404, 'Not found')
        request_json = request.get_json()
        if request_json is None:
            abort(400, 'Not a JSON')
        user_id = request_json.get("user_id")
        if user_id is None:
            abort(400, 'Missing user_id')
        user = storage.get("User", user_id)
        if user is None:
            abort(404, 'Not found')
        text = request_json.get("text")
        if text is None:
            abort(400, 'Missing_text')
        Review = CNC.get("Review")
        request_json['place_id'] = place_id
        new_review = Review(**request_json)
        new_review.save()
        return jsonify(new_review.to_json()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review_by_id(review_id):
    """A route the retrive a review, delete a review
    or update a review using the review id.
    Parameter:
        review_id: string(uuid), the id of review
    Return:
        for GET: a review object in json format
        for DELETE: an empty json
        for PUT: json format of updated review
    """
    review = storage.get("Review", review_id)

    if review is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(review.to_json())

    if request.method == 'DELETE':
        review.delete()
        del review
        return jsonify({})

    if request.method == 'PUT':
        request_json = request.get_json()
        if request_json is None:
            abort(400, 'Not a JSON')
        review = bm_update(request_json)
        return jsonify(review.to_json()), 200
