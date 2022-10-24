#!/usr/bin/python3
"""Module for Place related endpoints"""
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, make_response, abort, request
from models import storage
from models.review import Review

model = "Review"
parent_model = "Place"


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET"])
def get_reviews(place_id):
    """GET /place api route"""
    return get_models(parent_model, place_id, "reviews")


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """GET /review api route"""
    return get_model(model, review_id)


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """DELETE /review api route"""
    return delete_model(model, review_id)


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["POST"])
def post_review(place_id):
    """POST /reviews api route"""
    required_data = {"text", "user_id"}
    return post_model(model, parent_model, place_id, required_data)


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def put_review(review_id):
    """PUT /reviews api route"""
    ignore_data = ["id", "created_at", "updated_at", "user_id", "place_id"]
    return put_model(model, review_id, ignore_data)
