#!/usr/bin/python3
"""
file for "/api/v1/amenities" API
with GET, POST, PUT and DELETE
for getting, posting, putting and deleting
Review objects in 'storage', imported from
'models', and saving those changes in the
'storage's database/JSON file.
"""
from models.user import User
from models.place import Place
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route(
        "/places/<place_id>/reviews",
        strict_slashes=False
    )
def all_place_reviews_in_JSON(place_id):
    """
    Returns all reviews related to
    the Place instance, with 'place_id'
    as its id, in 'storage'.

    If the place doesn't exist,
    this function calls 'flask.abort(404)'.
    """
    reviewed_place = storage.get(Place, place_id)
    if not reviewed_place:
        # if reviewed_place doesn't exist
        abort(404)

    return jsonify(
        [
            review.to_dict()
            for review in
            reviewed_place.reviews
        ]
    )


@app_views.route(
        "/reviews/<review_id>",
        strict_slashes=False,
        methods=["GET"]
    )
def get_review_by_id_in_JSON(review_id):
    """
    Returns the review with the 'review_id'
    argument and route in 'storage',
    in its JSON-serializable dict form,
    if the 'Review' object exists.

    Raises 404 otherwise.
    """
    result = storage.get(Review, review_id)

    if result is None:
        abort(404)

    return jsonify(result.to_dict())


@app_views.route(
        "/reviews/<review_id>",
        strict_slashes=False,
        methods=["DELETE"]
    )
def delete_review_by_id(review_id):
    """
    Deletes 'Review' object with 'review_id' as its 'id'
    field/column value (let's call it 'target')
    from 'storage.all' dictionary, by calling storage.delete(<target>).

    Returns ({}, 200) if successful,
    404 if 'target' doesn't exist.
    """
    target = storage.get(Review, review_id)

    if target is None:
        abort(404)
    storage.delete(target)
    storage.save()

    return jsonify({}), 200


@app_views.route(
        "/places/<place_id>/reviews",
        strict_slashes=False,
        methods=["POST"]
    )
def post_review_in_JSON(place_id):
    """
    Creates new 'Review' object related
    to the Place instance in 'storage'
    with 'place_id' as its 'id'.

    If the input provided isn't valid JSON
    or if the JSON provided has no 'name' key,
    this function calls 'flask.abort(400)',
    with a message of what went wrong:
    either "Not a JSON" or "Missing name".
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    new_review_in_JSON = request.get_json(silent=True)
    # If the request's JSON isn't valid,
    # 'new_review_in_JSON' is None.
    if new_review_in_JSON is None:
        abort(400, "Not a JSON")

    if 'user_id' not in new_review_in_JSON:
        abort(400, "Missing user_id")

    new_review_user = storage.get(User, new_review_in_JSON['user_id'])
    if new_review_user is None:
        abort(404)

    if 'text' not in new_review_in_JSON:
        abort(400, "Missing text")

    new_review = Review(**new_review_in_JSON)
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>",
        strict_slashes=False,
        methods=["PUT"]
    )
def put_review_in_JSON(review_id):
    """
    Overrides 'Review' object's 'name' fields,
    where the object's id is 'review_id',
    with the json attributes provided in the
    PUT request.

    If the review with 'review_id' as its 'id'
    doesn't exist, this function calls
    abort(404).

    Otherwise, this function returns the JSON
    format of the new review with code 200.
    """
    if storage.get(Review, review_id) is None:
        abort(404)

    new_review_info = request.get_json(silent=True)
    if new_review_info is None:
        # not a valid JSON PUT request
        abort(400, "Not a JSON")

    review = storage.get(Review, review_id)
    # We're changing these attributes in place.
    for attr, value in new_review_info:
        if attr not in ('id', 'user_id',
                        'place_id', 'created_at',
                        'updated_at'):
            review.__setattr__(attr, value)

    storage.save()
    # We have to re-write the object change
    # to the database/storage file,
    # so that the changes are saved
    # there too, and not just in this
    # Python object.

    return jsonify(review.to_dict()), 200
