#!/usr/bin/python3
"""script that handles Review objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """retrieves all Review objects by place
    Args:
        place_id: place id"""
    list_of_reviews = []
    if not storage.get("Place", str(place_id)):
        abort(404)
    objs = storage.get("Place", str(place_id))
    for obj in objs.reviews:
        list_of_reviews.append(obj.to_dict())
    return jsonify(list_of_reviews)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def review_create(place_id):
    """create REview route
    Args:
        place_id: place id"""
    json_revs = request.get_json(silent=True)
    if json_revs is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", str(place_id)):
        abort(404)
    if "user_id" not in json_revs:
        abort(400, 'Missing user_id')
    if not storage.get("User", json_revs["user_id"]):
        abort(404)
    if "text" not in json_revs:
        abort(400, 'Missing text')
    json_revs["place_id"] = place_id
    new_review = Review(**json_revs)
    new_review.save()
    response = jsonify(new_review.to_dict())
    response.status_code = 201
    return response


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def review_by_id(review_id):
    """gets a specific Review object by ID
    Args:
        review_id: place object id """
    if not storage.get("Review", str(review_id)):
        abort(404)
    objs = storage.get("Review", str(review_id))
    return jsonify(objs.to_dict())


@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def review_put(review_id):
    """updates specific Review object by ID
    Args:
        review_id: Review object ID"""
    json_pls = request.get_json(silent=True)
    if json_pls is None:
        abort(400, 'Not a JSON')
    if not storage.get("Review", str(review_id)):
        abort(404)
    objs = storage.get("Review", str(review_id))
    for k, v in json_pls.items():
        if k not in ["id", "created_at", "updated_at", "user_id",
                     "place_id"]:
            setattr(objs, k, v)
    objs.save()
    return jsonify(objs.to_dict()), 200


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def review_delete_by_id(review_id):
    """deletes Review by id
    Args:
        Review object id"""
    if not storage.get("Review", str(review_id)):
        abort(404)
    objs = storage.get("Review", str(review_id))
    storage.delete(objs)
    storage.save()
    return jsonify({}), 200
