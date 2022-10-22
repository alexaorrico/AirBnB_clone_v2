#!/usr/bin/python3
""" index module """


from api.v1.views import review_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@review_views.route('reviews', strict_slashes=False)
def get_reviews():
    """ returns a list of all the reviews in db """
    reviews = storage.all(Review)
    lst = [review.to_dict() for review in reviews.values()]
    return jsonify(lst)


@review_views.route('reviews/<review_id>', strict_slashes=False)
def get_review_with_id_eq_review_id(review_id):
    """ returns a review with id == review_id """
    review = storage.get(Review, review_id)
    return jsonify(review.to_dict()) if review else abort(404)


@review_views.route('reviews/<review_id>', strict_slashes=False,
                    methods=["DELETE"])
def delete_review_with_id_eq_review_id(review_id):
    """ deletes a review with id == review_id """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@review_views.route('reviews', strict_slashes=False,
                    methods=["POST"])
def create_review():
    """ creates a new review """
    abort(405)
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400
    name = data.get("name")
    if not name:
        return jsonify({
            "error": "Missing name"
            }), 400
    review = Review(name=name)
    review.save()
    return jsonify(
        review.to_dict()
        ), 201


@review_views.route('reviews/<review_id>', strict_slashes=False,
                    methods=["PUT"])
def update_review_with_id_eq_review_id(review_id):
    """ updates a review's record """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400

    review_dict = review.to_dict()
    dont_update = ["id", "created_at", "updated_at", "user_id", "place_id"]
    for skip in dont_update:
        data[skip] = review_dict[skip]
    review_dict.update(data)
    review.delete()
    storage.save()
    updated_review = Review(**review_dict)
    updated_review.save()
    return jsonify(
            updated_review.to_dict()
            )


@review_views.route('places/<place_id>/reviews', strict_slashes=False)
def get_reviews_of_place(place_id):
    """ returns list of reviews associated with place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(
                [review.to_dict() for review in place.reviews]
            )


@review_views.route('places/<place_id>/reviews', strict_slashes=False,
                    methods=["POST"])
def create_linked_to_place_review(place_id):
    """ returns list of reviews associated with place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
                "error": "Not a JSON"
            }), 400
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({
                "error": "Missing user_id"
            }), 400

    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not data.get("text"):
        return jsonify({
                "error": "Missing text"
            }), 400

    review = Review(**data)
    dct = review.to_dict()
    place.reviews.append(review)
    # review.place_id = place.id
    review.save()
    place.save()
    return(
        jsonify(dct)
        ), 201
