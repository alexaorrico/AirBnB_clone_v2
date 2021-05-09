#!/usr/bin/python3
"""creates a new view for Review objects"""
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models import storage
from flask import jsonify, abort


@app_views.route('/places/<place_id>/reviews', methods=["GET"],
                 strict_slashes=False)
def city_list(place_id):
    """retrieves the list of all review objects of a place object"""
    placeobj = storage.get(Place, place_id)
    if placeobj is None:
        abort(404)
    return jsonify(placeobj.reviews)


@app_views.route('/reviews/<review_id>', methods=["GET"],
                 strict_slashes=False)
def city(review_id):
    """retrieves a review object"""
    try:
        reviewobj = storage.get(Review, review_id).to_dict()
        return jsonify(reviewobj)
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=["DELETE"],
                 strict_slashes=False)
def city(review_id):
    """deletes a review object"""
    reviewobj = storage.get(Review, review_id)
    if reviewobj is not None:
        storage.delete(reviewobj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=["POST"],
                 strict_slashes=False)
def create(place_id):
    """creates a review object"""
    try:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        body_dict = request.get_json()
        if "user_id" not in body_dict:
            return jsonify({"error": "Missing user_id"}), 400
        if storage.get(User, body_dict["user_id"]) is None:
            abort(404)
        if "text" not in body_dict:
            return jsonify({"error": "Missing text"}), 400
        if storage.get(Place, place_id) is None:
            abort(404)
        reviewobj = Review(name=body_dict["name"],
                           place_id=body_dict["place_id"]
                           user_id=body_dict["user_id"])
        reviewobj.save()
        return jsonify(reviewobj.to_dict()), 201
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=["PUT"],
                 strict_slashes=False)
def update(review_id):
    """updates existing review object"""
    reviewobj = storage.get(Review, review_id)
    if reviewobj is None:
        abort(404)
    body_dict = request.get_json()
    if body_dict is None:
        abort(400, "Not a JSON")
    body_dict.pop("id", None)
    body_dict.pop("user_id", None)
    body_dict.pop("place_id", None)
    body_dict.pop("created_at", None)
    body_dict.pop("updated_at", None)
    for key, value in body_dict.items():
        setattr(reviewobj, key, value)
    reviewobj.save()
    return jsonify(reviewobj.to_dict()), 200
