#!/usr/bin/python3
'''Module containing instructions for the flask blueprint app_views'''
from api.v1.views import app_views
from api import mapped_classes
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def all_reviews(place_id):
    '''Retrieves all Review objects associated with place_id'''
    content = storage.get("Place", place_id)
    if content is None:
        abort(404)
    else:
        info = content.places
        rqd_info = []
        for item in info:
            rqd_info.append(item.to_dict())
        return jsonify(rqd_info)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def post_make_new_review(place_id):
    '''Create a Review object with the values provided'''
    json_content = request.get_json()
    if not json_content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in json_content:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if storage.get("User", json_content["user_id"]) is None:
        abort(404)
    if "text" not in json_content:
        return make_response(jsonify({"error": "Missing text"}), 400)
    content = storage.get("Place", place_id)
    if content is None:
        abort(404)
    json_content["place_id"] = place_id
    new_review = mapped_classes["Review"](**json_content)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/review/<review_id>', strict_slashes=False, methods=['GET'])
def get_specific_review(review_id):
    '''Get a specific review by the id given'''
    content = storage.get("Review", review_id)
    if content is None:
        abort(404)
    else:
        return jsonify(content.to_dict())


@app_views.route('/review/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_spcific_review(review_id):
    '''Delete a specific review else raise an error'''
    content = storage.get("Review", review_id)
    if content is None:
        abort(404)
    else:
        storage.delete(content)
        storage.save()
        return jsonify({}), 200


@app_views.route('/review/<review_id>', strict_slashes=False, methods=['PUT'])
def update_specified_review(review_id):
    '''Update a sepcific review as identified by ID'''
    content = storage.get("Review", review_id)
    if content is None:
        abort(404)
    else:
        update_dict = request.get_json()
        if not update_dict:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        update_dict.pop("id", None)
        update_dict.pop("created_at", None)
        update_dict.pop("updated_at", None)
        update_dict.pop("place_id", None)
        update_dict.pop("user_id", None)
        for key, value in update_dict.items():
            setattr(content, key, value)
        content.save()
        return jsonify(content.to_dict()), 200
