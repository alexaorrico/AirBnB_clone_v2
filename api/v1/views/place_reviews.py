#!/usr/bin/python3
"""Routing for AirBnB review object"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    """'GET' response"""
    dic = storage.all(Review)
    if request.method == 'GET':
        if review_id is None:
            reviews_list = []
            for key, value in dic.items():
                reviews_list.append(value.to_dict())
            return jsonify(reviews_list)
        else:
            for key, value in dic.items():
                if value.id == review_id:
                    return jsonify(value.to_dict())
            abort(404)


@app_views.route(
    '/reviews/<review_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_review(review_id=None):
    """'DELETE' response"""
    dic = storage.all(Review)
    if request.method == 'DELETE':
        empty = {}
        if review_id is None:
            abort(404)
        for key, value in dic.items():
            if value.id == review_id:
                storage.delete(value)
                storage.save()
                return jsonify(empty), 200
        abort(404)


@app_views.route('/reviews', methods=['POST'], strict_slashes=False)
def post_review():
    """'POST' response"""
    dic = storage.all(Review)
    flag = 0
    if not request.json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    for key in body:
        if key == 'name':
            flag = 1
    if flag == 0:
        abort(400, "Missing name")
    new_review = Review(**body)
    storage.new(new_review)
    storage.save()
    new_review_dic = new_review.to_dict()
    return jsonify(new_review_dic), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id=None):
    """'PUT' response"""
    dic = storage.all(Review)
    if not request.json:
        abort(400, 'Not a JSON')
    body = request.get_json()
    for key, value in dic.items():
        if value.id == review_id:
            for k, v in body.items():
                setattr(value, k, v)
            storage.save()
            return jsonify(value.to_dict()), 200
    abort(404)
