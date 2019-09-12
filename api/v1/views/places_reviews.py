#!/usr/bin/python3
""" API REST for Reviews """
from models import storage
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews')
def reviews_id(place_id):
    """ Route return all reviews in place referenced id """
    my_place = storage.get('Place', place_id)
    try:
        return jsonify(list(map(lambda x: x.to_dict(), my_place.reviews)))
    except:
        abort(404)


@app_views.route('/reviews/<review_id>')
def reviews_id(review_id):
    """ Route return reviews with referenced id """
    my_review = storage.get('Review', review_id)
    try:
        return jsonify(my_review.to_dict())
    except:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_city_id(review_id):
    """ Route delete reviews with referenced id """
    my_object = storage.get('Review', review_id)
    if my_object is not None:
        storage.delete(my_object)
        storage.save()
    else:
        abort(404)
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_cities(state_id):
    """ Route create cities with POST"""
    if request.is_json:
        data = request.get_json()
        if not storage.get("State", state_id):
            abort(404)
        if 'name' in data:
            data["state_id"] = state_id
            new_city = City(**data)
            new_city.save()
            return jsonify(new_city.to_dict()), 201
        else:
            return jsonify(error="Missing name"), 400
    else:
        return jsonify(error="Not a JSON"), 400


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_cities(city_id):
    """ Route update cities with PUT """

    if request.is_json:
        data = request.get_json()
        my_object = storage.get('City', city_id)
        if my_object is not None:
            for keys, values in data.items():
                if keys not in ["created_at", "updated_at", "id"]:
                    setattr(my_object, keys, values)
            my_object.save()
            return jsonify(my_object.to_dict()), 200
        else:
            abort(404)
    else:
        return jsonify(error="Not a JSON"), 400
