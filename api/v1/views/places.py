#!/usr/bin/python3
""" index module """


from api.v1.views import place_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@place_views.route('places', strict_slashes=False)
def get_places():
    """ returns a list of all the places in db """
    places = storage.all(Place)
    lst = [place.to_dict() for place in places.values()]
    return jsonify(lst)


@place_views.route('places/<place_id>', strict_slashes=False)
def get_place_with_id_eq_place_id(place_id):
    """ returns a place with id == place_id """
    place = storage.get(Place, place_id)
    return jsonify(place.to_dict()) if place else abort(404)


@place_views.route('places/<place_id>', strict_slashes=False,
                   methods=["DELETE"])
def delete_place_with_id_eq_place_id(place_id):
    """ deletes a place with id == place_id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@place_views.route('places', strict_slashes=False,
                   methods=["POST"])
def create_place():
    """ creates a new place """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400
    abort(405)
    name = data.get("name")
    if not name:
        return jsonify({
            "error": "Missing name"
            }), 400
    place = Place(name=name)
    place.save()
    return jsonify(
        place.to_dict()
        ), 201


@place_views.route('places/<place_id>', strict_slashes=False,
                   methods=["PUT"])
def update_place_with_id_eq_place_id(place_id):
    """ updates a place's record """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400

    place_dict = place.to_dict()
    dont_update = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for skip in dont_update:
        data[skip] = place_dict[skip]
    place_dict.update(data)
    place.delete()
    storage.save()
    updated_place = Place(**place_dict)
    updated_place.save()
    return jsonify(
            updated_place.to_dict()
            )


@place_views.route('cities/<city_id>/places', strict_slashes=False)
def get_places_of_city(city_id):
    """ returns list of places associated with city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(
                [place.to_dict() for place in city.places]
            )


@place_views.route('cities/<city_id>/places', strict_slashes=False,
                   methods=["POST"])
def create_linked_to_city_place(city_id):
    """ returns list of places associated with city """
    city = storage.get(City, city_id)
    if not city:
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
    if not data.get("name"):
        return jsonify({
                "error": "Missing name"
            }), 400

    place = Place(**data)
    dct = place.to_dict()
    city.places.append(place)
    # place.city_id = city.id
    place.save()
    city.save()
    return(
        jsonify(dct)
        ), 201
