#!/usr/bin/python3

"""Reviews API Routes"""

from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
    '/places/<place_id>/reviews/', methods=['GET'], strict_slashes=False)
def show_reviews(place_id):
    """Show all review in storage"""
    reviews_list = []
    place = storage.get("Place", place_id)
    if place:
        for review in place.reviews:
            reviews_list.append(review.to_dict())
        return jsonify(reviews_list)
    else:
        abort(404)


@app_views.route(
    '/reviews/<review_id>/', methods=['GET'], strict_slashes=False)
def display_review(review_id):
    """Displays an existing review based on id from storage"""
    review = storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route(
    '/reviews/<review_id>/', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete an existing review"""
    review = storage.get("Review", review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route(
    '/places/<place_id>/reviews/', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a new reviews"""
    error_message = ""
    place = storage.get("Place", place_id)
    if place:
        content = request.get_json(silent=True)
        if type(content) is dict:
            if "user_id" not in content.keys():
                error_message = "Missing user_id"
            elif "text" not in content.keys():
                error_message = "Missing text"
            else:
                user = storage.get("User", content['user_id'])
                if user:
                    review = Review(**content)
                    review.place_id = place_id
                    storage.new(review)
                    storage.save()
                    response = jsonify(review.to_dict())
                    response.status_code = 201
                    return response

                else:
                    abort(404)
        else:
            error_message = "Not a JSON"
        response = jsonify({"error": error_message})
        response.status_code = 400
        return response
    else:
        abort(404)


@app_views.route(
    '/reviews/<review_id>/', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates an existing review based on id from storage"""
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    review = storage.get("Review", review_id)
    if review:
        content = request.get_json(silent=True)
        if type(content) is dict:
            for key, value in content.items():
                if key not in ignore:
                    setattr(review, key, value)
            storage.save()
            return jsonify(review.to_dict())

        else:
            response = jsonify({"error": "Not a JSON"})
            response.status_code = 400
            return response
    else:
        abort(404)
