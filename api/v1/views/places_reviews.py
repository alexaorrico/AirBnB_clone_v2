#!/usr/bin/python3
""" handles all default RESTFul API actions """
from models import user
import models
from os import abort, stat
from flask import json
from sqlalchemy.sql.sqltypes import String
from models.review import Review
from flask.json import jsonify
from api.v1.views import app_views
from flask import request, abort


@app_views.route(
    '/reviews/<review_id>',
    strict_slashes=False,
    methods=['GET', 'POST', 'PUT', 'DELETE']
    )
def manipulate_review(review_id=None):
    from models import storage
    obj_review = storage.get('Review', review_id)
    if obj_review is None:
        abort(404, 'Not Found')
    if request.method == "GET":
        return jsonify(obj_review.to_dict())
    if request.method == "DELETE":
        obj_review.delete()
        storage.save()
        return jsonify({})
    if request.method == "PUT":
        json_req = request.get_json()
        if json_req is None:
            abort(400, 'Not a JSON')
        obj_review.update(json_req)
        return jsonify(user.to_dict()), 200


@app_views.route(
    '/places/<place_id>/reviews',
    strict_slashes=False,
    methods=['GET', 'POST']
    )
def manipulate_place_id(place_id=None):
    from models import storage

    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404, 'Not found')
    if request.method == "GET":
        all_reviews = storage.all('Review')
        l = []
        for review in all_reviews.values():
            if review.place_id == place_id:
                l.append(review.to_dict())
        return jsonify(l)
    if request.method == "POST":
        json_req = request.get_json()
        if json_req is None:
            abort(400, 'Not a JSON')
        if json_req.get("text") is None:
            abort(400, 'Missing text')
        if json_req.get("user_id") is None:
            abort(400, 'Missing user_id')
        user_id = json_req.get("user_id")
        user_obj = storage.get('User', user_id)
        if user_obj is None:
            abort(400)
        json_req["place_id"] = place_id
        new_obj = Review(**json_req)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201
