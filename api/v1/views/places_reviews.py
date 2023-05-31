#!/usr/bin/python3

"""
a new view for Review object that handles all default RESTFul API actions
"""

from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from flask import jsonify, abort, make_response


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def retrieve_review_uisng_placeid(place_id):
    """
    retrieves all review objects of a place
    raises a 404 error if the place_id isnt linked to any review
    """

    review_list = []
    place = storage.get(Place, place_id)
    if place:
        for reviewid in place.reviews:
            review_list.append(reviewid.to_dict())
        return jsonify(review_list)
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def retrieve_review(review_id):
    """
    Retrieves a review using the review id
    Raises a 404 error if the review_id isnt linked to any review
    """

    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """
    delets a review
    """

    review = storage.get(Review, review_id)
    if review:
        review.delete()
        storage.save()
        return jsonify({})
    abort(404)
