#!/usr/bin/python3
""" Place view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=[
                        'GET', 'POST'])
def all_place_reviews(place_id=None):
    """ retrieves all Place Reviews """

    places_list = storage.all("Place").values()

    try:
        place = storage.all("Place").pop("Place." + place_id)
    except KeyError:
        abort(404)

    if request.method == "GET":
        my_place_reviews = [review.to_dict() for review in place.reviews]
        return (jsonify(my_place_reviews))

    if request.method == "POST":
        try:
            data = request.get_json(silent=True)
        except:
            return (jsonify({"error": "Not a JSON"}), 400)

        users = [user.id for user in storage.all("User").values()]

        if "user_id" not in data.keys():
            return (jsonify({"error": "Missing user_id"}), 400)
        if "text" not in data.keys():
            return (jsonify({"error": "Missing text"}), 400)
        if data.get("user_id") not in users:
            abort(404)
        review = Review(**data)
        review.save()
        return (jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=[
                    'GET', 'DELETE', 'PUT'])
def a_review(review_id):
    """ retrieves all Places """

    reviews_list = storage.all("Review").values()

    try:
        review = storage.all("Review").pop("Review." + review_id)
    except KeyError:
        abort(404)

    if request.method == 'GET':
        return (jsonify(review.to_dict()))

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return (jsonify({}), 200)

    data = request.get_json(silent=True)
    if not data:
        return (jsonify({"error": "Not a JSON"}), 400)

    if request.method == 'PUT':
        for k, v in data.items():
            if k not in [
                    'id', 'user_id', 'created_at', 'updated_at', 'place_id']:
                setattr(place, k, v)
        storage.new(review)
        storage.save()
        return (jsonify(review.to_dict()), 200)
