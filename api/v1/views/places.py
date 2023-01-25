#!/usr/bin/python3
"""Places API"""
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from . import app_views
from flask import jsonify, abort, request

@app_views.route("/cities/<city_id>/places")
def places(city_id):
    """Get all the places of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    place_list = []
    for place in places:
        place_list.append(place.to_dict())
    return jsonify(place_list)

@app_views.route("/places/<place_id>")
def place(place_id):
    """Get a single place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Delete a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})

@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """Create a place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Mising name")
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201

@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Update a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if "id" in data:
        data.pop("id")
    if "city_id" in data:
        data.pop("city_id")
    if "user_id" in data:
        data.pop("user_id")
    if "created_at" in data:
        data.pop("created_at")
    if "updated_at" in data:
        data.pop("updated_at")
    for key, value in data.items():
        place.__setattr__(key, value)
    place.save()
    return jsonify(place.to_dict())

@app_views.route("/places/<place_id>/amenities")
def place_amenities(place_id):
    """Get amenities of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = place.amenities
    amenity_list = []
    for amenity in amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)

@app_views.route("/places/<place_id>/amenities/<amenity_id>")
def delete_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})

@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def link_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if storage.get(Place, amenity.place_id):
        return jsonify(amenity.to_dict())
    amenity.place_id = place_id
    amenity.save()
    return jsonify(amenity.to_dict()), 201