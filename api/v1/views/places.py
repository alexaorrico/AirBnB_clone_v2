#!/usr/bin/python3
""" Your first endpoint (route) will be to return the status of your API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.amenity import Amenity
import json

@app_views.route("/cities/<city_id>/places/", methods=['GET', 'POST'])
@app_views.route("/cities/<city_id>/places", methods=['GET', 'POST'])
def show_places(city_id):
    """ returns list of places """
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    if request.method == 'GET':
        lista = []
        for place in cities.places:
            lista.append(place.to_dict())
        return jsonify(lista)
    elif request.method == 'POST':
        if request.json:
            new_dict = request.get_json()
            if "user_id" in new_dict.keys():
                users = storage.all(User).values()
                for user in users:
                    if new_dict['user_id'] == user.id:
                        if "name" in new_dict.keys():
                            new_dict['city_id'] = city_id
                            new_place = Place(**new_dict)
                            storage.new(new_place)
                            storage.save()
                            return jsonify(new_place.to_dict()), 201
                        else:
                            abort(400, description="Missing name")
                abort(404)
            else:
                abort(400, description="Missing user_id")
        else:
            abort(400, description="Not a JSON")

@app_views.route("places/<place_id>/", methods=['GET', 'DELETE', 'PUT'])
@app_views.route("places/<place_id>", methods=['GET', 'DELETE', 'PUT'])
def show_place(place_id):
    """ returns state data """
    if request.method == 'GET':
        places = storage.all(Place).values()
        for place in places:
            if place.id == place_id:
                return jsonify(place.to_dict())
        abort(404)
    elif request.method == 'DELETE':
        places = storage.all(Place).values()
        for place in places:
            if place.id == place_id:
                place.delete()
                storage.save()
                return jsonify({}), 200
        abort(404)
    elif request.method == 'PUT':
        if request.json:
            new_dict = request.get_json()
            place = storage.get(Place, place_id)
            if place:
                no = ['id', 'user_id', 'city_id', 'created_at', 'updated_id']
                for key, value in new_dict.items():
                    if key not in no:
                        setattr(place, key, value)
                storage.save()
                return jsonify(place.to_dict()), 200
            abort(404)
        else:
            abort(400, description="Not a JSON")

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def St_Ci_Am_places():
    """ Function to search places containing one of """
    new_dict = request.get_json()
    if new_dict is None:
        abort(400, description="Not a JSON")
    
    counter = 0
    for lists in new_dict.values():
        if lists != []:
            counter += 1

    if len(new_dict) == 0 or counter == 0:
        all_places = []
        places = storage.all(Place)
        for place in places.values():
            all_places.append(place.to_dict())
        return jsonify(all_places)

    lista = []
    if "states" in new_dict.keys() and len(new_dict["states"]) > 0:
        for values in new_dict["states"]:
            states = storage.get(State, values)
            for city in states.cities:
                for place in city.places:
                    lista.append(place.to_dict())
    
    if "cities" in new_dict.keys() and len(new_dict["cities"]) > 0:
        for val in new_dict["cities"]:
            cities = storage.get(City, val)
            for place in cities.places:
                if place not in lista:
                    lista.append(place.to_dict())

    if "amenities" in new_dict.keys() and len(new_dict["amenities"]) > 0:
        cities = storage.all(City).values()
        for citi in cities:
            for place in citi.places:
                flag = 0
                lista_amen = []
                place_i = place.to_dict()
                for amen in place.amenities:
                    lista_amen.append(amen)
                for v in new_dict["amenities"]:
                    ameniti = storage.get(Amenity, v)
                    if ameniti not in lista_amen:
                        flag = 1
                        break
                if flag == 0:
                    if place not in lista:
                        lista.append(place_i)
    return jsonify(lista)
