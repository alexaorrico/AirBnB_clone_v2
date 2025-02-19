#!/usr/bin/python3
"""
Route for handling Review objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review

@app_views.route("/places/<place_id>/reviews", methods=["GET"],
        strict_slashes=False)
def reviews_by_place(place_id):
    """
    Retrieves all Review objects by place
    :return JSON list of all cities
    """
    review_list = []
    place_obj = storage.get("Place", str(place_id))
    if place_obj is None:
        abort(404)
    for obj in place_obj.reviews:
        review_list.append(obj.to_dict())
    return jsonify(review_list)

@app_views.route("/places/<place_id>/reviews", methods=["POST"],
        strict_slashes=False)
def review_create(place_id):
    """
    Create Reviews rout
    
    :return: JSON of the newly created object
    """
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if not storage.get("User", review_json["user_id"]):
        abort(404)
    if "user_id" not in review_json:
        abort(400, "Missing user_id")
    if 'text' not in review_json:
        abort(400, 'Missing text')

    review_json["place_id"] = place_id

    # create a new place object using the JSON data
    new_review = Review(**review_json)
    new_review.save()

    # Return the new review object as JSON with 202 status code
    resp = jsonify(new_review.to_dict())
    resp.status_code = 201

    return resp

@app_views.route("/reviews/<review_id>", methods=["GET"],
                strict_slashes=False)
def review_by_id(review_id):
    """
    Retrieve specific review object by ID
    :param review_id: place object ID
    :return: JSON of the review objects with the specific id or 404 error

    """
    # Fetch the place objects by ID
    fetched_obj = storage.get("Review", str(review_id))
    # if the object is not found return 404 error
    if fetched_obj is None:
        abort(404)

    # Return the state object as JSON
    return jsonify(fetched_obj.to_dict())

@app_views.route("/reviews/<review_id>", methods=["PUT"],
        strict_slashes=False)
def review_put(review_id):
    """
    Update a specific review object by ID
    :param review_id: review objects ID
    :return: JSON of the updated place object and 200 on success
    or 400 0r 404 on failure
    """
    # Get the JSON request body
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("Review", str(review_id))
    if fetched_obj is None:
        abort(404)
    # update the place object with new values , ignoring certain keys
    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                "place_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    # Return the updated place object as JSON
    return jsonify(fetched_obj.to_dict())

@app_views.route("/reviews/<review_id>", methods=["DELETE"],
        strict_slashes=False)
def review_delete_by_id(review_id):
    """
    Delete a place object by ID
    :param place_id: city object ID
    :return Empty dictionary with 200 status code or 404 if not found

    """
    # Fetch the state object by ID
    fetched_obj = storage.get("Review", str(review_id))
    if fetched_obj is None:
        abort(404)

    # Delete the city object
    storage.delete(fetched_obj)
    storage.save()

    # Return an empty dictionary with a 200 status code
    return jsonify({})

