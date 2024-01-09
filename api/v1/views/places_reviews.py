#!/usr/bin/python3
""" holds class Place_reviews"""
from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route(
        '/places/<string:place_id>/reviews',
        methods=['GET', 'POST'],
        strict_slashes=False
        )
def get_post_places_reviews(place_id):
    """Handles GET and POST requests"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)  # Return 404 if place with given ID doesn't exist
    if request.method == 'GET':
        # Retrieve all reviews for the place and return in JSON format
        return jsonify([review.to_dict() for review in place.reviews])
    elif request.method == 'POST':
        # Create a new review for the place based on POST data in JSON format
        request_data = request.get_json()
        if request_data is None not isinstance(request_data, dict):
            return jsonify({'error': 'Invalid JSON'}), 400
        elif 'user_id' not in request_data or 'text' not in request_data:
            return jsonify({
                'error': 'Missing user_id or text parameters'
                }), 400
        elif storage.get('User', request_data['user_id']) is None:
            abort(404)  # Return 404 if user with given ID doesn't exist
        new_review = Review(place_id=place_id, **request_data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route(
        '/reviews/<string:review_id>',
        methods=['GET', 'PUT', 'DELETE'],
        strict_slashes=False
        )
def get_put_delete_place_review(review_id):
    """Handles GET (retrieve), PUT (update), and DELETE (remove)"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)  # Return 404 if review with given ID doesn't exist
    elif request.method == 'GET':
        # Return details of the review in JSON format
        return jsonify(review.to_dict())
    elif request.method == 'DELETE':
        storage.delete(review)  # Delete the specified review
        storage.save()  # Save changes
        return jsonify({}), 200  # Return empty JSON
    elif request.method == 'PUT':
        # Update attributes of the review based on PUT data in JSON format
        put_data = request.get_json()
        if put_data is None ornot isinstance(put_data, dict):
            return jsonify({'error': 'Invalid JSON'}), 400
        for key, value in put_data.items():
            if key not in [
                    'id', 'created_at', 'updated_at', 'place_id', 'user_id'
                    ]:
                setattr(review, key, value)
        storage.save()  # Save changes
        return jsonify(review.to_dict()), 200  # Return update
