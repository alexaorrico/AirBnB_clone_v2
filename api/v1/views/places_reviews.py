#!/usr/bin/python3
"""Routes for Amenities"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['GET'])
def showReview(place_id):
    """ Shows all reviews for a place in the file storage """
    count_l = []
    pl_rev = storage.get("Place", place_id)
    if pl_rev is None:
        abort(404)
    eachReview = storage.all("Review")
    for value in eachReview.values():
        if value.place_id == place_id:
            count_l.append(value.to_dict())
    return(jsonify(count_l))


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['GET'])
def a_review_id(review_id):
    """ Gets the review and its id if any """
    i = storage.get("Review", review_id)
    if i:
        return jsonify(i.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=["DELETE"])
def del_review_id(review_id):
    """ deletes a review if given the id """
    thing = storage.all('Review')
    revy = "Review." + review_id
    revs = thing.get(revy)
    if revs is None:
        abort(404)
    else:
        revs.delete()
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['POST'])
def postReview(place_id):
    """ creates a new Review """
    if storage.get("Place", place_id) is None:
        abort(404)
    thing = request.get_json()
    if not thing:
        return (jsonify({"error": "Not a JSON"}), 400)
    user = thing.get("user_id")
    if user is None:
        return (jsonify({"error": "Missing user_id"}), 400)
    useConfirm = storage.get("User", user)
    if useConfirm is None:
        abort(404)
    review = thing.get("text")
    if review is None or len(thing) == 0:
        return (jsonify({"error": "Missing text"}), 400)
    r = Review()
    r.user_id = user
    r.place_id = place_id
    r.text = review
    r.save()
    return (jsonify(r.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=["PUT"])
def updateReview(review_id):
    """ updates the review info, specifically name """
    # garbage = {"id", "created_at", "updated_at"}
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    thing = request.get_json()
    if not thing:
        return (jsonify({"error": "Not a JSON"}), 400)
    for key, value in thing.items():
        if key == 'text':
            setattr(review, key, value)
    review.save()
    return (jsonify(review.to_dict()), 200)
