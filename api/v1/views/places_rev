#!/usr/bin/python3
""" Route for handling place reviews """
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """
    Retrieves all Review objects by place.
    :param place_id: ID of the place
    :return: JSON of all reviews
    """

    list_of_reviews = []
    obj_place = storage.get("Place", str(place_id))

    if obj_place is None:
        abort(404)

    for obj in obj_place.reviews:
        # Use to_dict instead of to_json
        list_of_reviews.append(obj.to_dict())

    return jsonify(list_of_reviews)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review object.
    :param place_id: ID of the place
    :return: Newly created Review object
    """

    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if not storage.get("User", review_json["user_id"]):
        abort(404)
    if "user_id" not in review_json:
        abort(400, 'Missing user_id')
    if "text" not in review_json:
        abort(400, 'Missing text')

    review_json["place_id"] = place_id

    new_review = Review(**review_json)
    new_review.save()
    # Fix the typo in response
    response = jsonify(new_review.to_dict())
    response.status_code = 201

    return response


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """
    Gets a specific Review object by ID.
    :param review_id: ID of the review
    :return: Review object with the specified ID or error
    """

    obj_fetched = storage.get("Review", str(review_id))

    if obj_fetched is None:
        abort(404)

    # Use to_dict instead of to_json
    return jsonify(obj_fetched.to_dict())


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review_by_id(review_id):
    """
    Updates a specific Review object by ID.
    :param review_id: ID of the review
    :return: Review object and 200 on success, or 400 or 404 on failure
    """

    # Use review_json instead of place_json
    review_json = request.get_json(silent=True)

    if review_json is None:
        abort(400, 'Not a JSON')

    obj_fetched = storage.get("Review", str(review_id))

    if obj_fetched is None:
        abort(404)

    for key, val in review_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(obj_fetched, key, val)

    obj_fetched.save()

    # Use to_dict instead of to_json
    return jsonify(obj_fetched.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """
    Deletes a Review by ID.
    :param review_id: ID of the review
    :return: Empty dictionary with 200, or 404 if not found
    """

    obj_fetched = storage.get("Review", str(review_id))

    if obj_fetched is None:
        abort(404)

    storage.delete(obj_fetched)
    storage.save()

    return jsonify({})
