#!/usr/bin/python3
""" Your first endpoint (route) will be to return the status of your API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.review import Review
import json

@app_views.route("/places/<place_id>/reviews/", methods=['GET', 'POST'])
@app_views.route("/places/<place_id>/reviews", methods=['GET', 'POST'])
def show_places(place_id):
    """ returns list of reviews """
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    if request.method == 'GET':
        lista = []
        for review in places.reviews:
            lista.append(review.to_dict())
        return jsonify(lista)
    elif request.method == 'POST':
        if request.json:
            new_dict = request.get_json()
            if "user_id" in new_dict.keys():
                users = storage.all(User).values()
                for user in users:
                    if new_dict['user_id'] == user.id:
                        if "text" in new_dict.keys():
                            new_review = City(**new_dict)
                            storage.new(new_review)
                            storage.save()
                            return jsonify(new_review.to_dict()), 201
                        else:
                            abort(400, description="Missing text")
                abort(404)
            else:
                abort(400, description="Missing user_id")
        else:
            abort(400, description="Not a JSON")

@app_views.route("reviews/<review_id>/", methods=['GET', 'DELETE', 'PUT'])
@app_views.route("reviews/<review_id>", methods=['GET', 'DELETE', 'PUT'])
def show_place(review_id):
    """ returns state data """
    if request.method == 'GET':
        reviews = storage.all(Review).values()
        for review in reviews:
            if review.id == review_id:
                return jsonify(review.to_dict())
        abort(404)
    elif request.method == 'DELETE':
        reviews = storage.all(Review).values()
        for review in reviews:
            if review.id == review_id:
                review.delete()
                storage.save()
                return jsonify({}), 200
        abort(404)
    elif request.method == 'PUT':
        if request.json:
            new_dict = request.get_json()
            review = storage.get(Review, review_id)
            if review:
                no = ['id', 'user_id', 'place_id', 'created_at', 'updated_id']
                for key, value in new_dict.items():
                    if key not in no:
                        setattr(review, key, value)
                storage.save()
                return jsonify(review.to_dict()), 200
            abort(404)
        else:
            abort(400, description="Not a JSON")
