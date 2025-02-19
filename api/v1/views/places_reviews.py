#!/usr/bin/python3
"""new view for Review object that handles all default"""

from api.v1.views import app_views
from models import storage
from flask import Flask, abort, jsonify, make_response
from models.review import Review
from models.place import Place
from models.city import City
from models.user import User
from flask import request
from models.state import State


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def all_review(place_id=None):
    """Return all reviews"""
    if place_id is not None:
        my_place_obj = storage.get(Place, place_id)
        if my_place_obj is None:
            abort(404)
        else:
            reviews = storage.all(Review).values()
            lista = []
            for review in reviews:
                if review.place_id == my_place_obj.id:
                    my_review_obj = storage.get(Review, review.id)
                    lista.append(my_review_obj.to_dict())
            return jsonify(lista)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def review_id_(review_id=None):
    """Return place id"""
    if review_id is not None:
        my_review_obj = storage.get(Review, review_id)
        if my_review_obj is None:
            abort(404)
        else:
            return jsonify(my_review_obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def review_delete(review_id=None):
    """DELETE review"""
    if review_id is not None:
        my_review_obj = storage.get(Review, review_id)
        if my_review_obj is None:
            abort(404)
        else:
            storage.delete(my_review_obj)
            return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def review_post(place_id=None):
    """POST review"""
    if place_id is not None:
        my_place_obj_ = storage.get(Place, place_id)
        if my_place_obj_ is None:
            abort(404)
        else:
            my_json = request.get_json(silent=True)
            if my_json is not None:
                if "user_id" in my_json:
                    my_user_obj_ = storage.get(User, my_json['user_id'])
                    if my_user_obj_ is not None:
                        if "text" in my_json:
                            text = my_json["text"]
                            n = Review(text=text, user_id=my_json['user_id'],
                                       place_id=place_id)
                            n.save()
                            return make_response(jsonify(n.to_dict()), 201)
                        else:
                            abort(400, "Missing text")
                    else:
                        abort(404)
                else:
                    abort(400, "Missing user_id")
            else:
                abort(400, "Not a JSON")


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_obj_review(review_id=None):
    """PUT review"""
    if review_id is not None:
        my_review_obj = storage.get(Review, review_id)
        if my_review_obj is None:
            abort(404)
        else:
            update_ = request.get_json(silent=True)
            if update_ is not None:
                for key, value in update_.items():
                    setattr(my_review_obj, key, value)
                    my_review_obj.save()
                return make_response(jsonify(my_review_obj.to_dict()), 200)
            else:
                abort(400, "Not a JSON")
