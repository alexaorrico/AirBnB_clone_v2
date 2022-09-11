#!/usr/bin/python3
"""file places_reviews"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
import json

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def review(place_id=None):
    """review function"""
    list_of_reviews = []
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    for review in places.reviews:
        list_of_reviews.append(review.to_dict())
    return jsonify(list_of_reviews)


@app_views.route('reviews/<review_id>', methods=['GET'], strict_slashes=False)
def reviewid(review_id=None):
    """review id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def reviewdel(review_id=None):
    """review delete"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def reviewpost(place_id=None):
    """review post"""
    body = request.get_json()
    if body is None:
        return jsonify({
            "error": "Not a JSON"
        }), 400
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if 'user_id' not in body:
        return jsonify({
            "error": "Missing user_id"
        }), 400
    user_id = body.get("user_id")
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if 'text' not in body.keys():
        return jsonify({
            "error": "Missing text"
        }), 400
    body['place_id'] = place_id
    body['user_id'] = user_id

    # Se crea una instancia de la clase Review
    obj = Review(**body)

    storage.new(obj)
    # Se guarda el nuevo objeto dentro del storage
    storage.save()

    # Se devuelve el objeto creado y un status code de 201
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def reviewput(review_id=None):
    """review put"""
    notAttr = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    body = request.get_json()
    if body is None:
        return jsonify({
            "error": "Not a JSON"
        }), 400
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    for key, value in body.items():
        if key not in notAttr:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
