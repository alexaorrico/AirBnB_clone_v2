#!/usr/bin/python3
"""
-----------------------
New view for Places
-----------------------
"""


from flask import jsonify, request, abort
from api.v1.views import app_views
from api.v1.views.aux_func import aux_func

methods = ["GET", "DELETE", "POST", "PUT"]


@app_views.route("/cities/<city_id>/places", methods=methods)
def places_city(city_id=None):
    """
    ------------------------
    Route for Places by city
    And Create a new place
    ------------------------
    """
    from models.place import Place
    from models.city import City
    from models.user import User
    from models import storage

    # places = storage.all(Place)
    city = storage.get(City, city_id)
    if request.method == 'GET':
        if city:
            places = [place.to_dict() for place in city.places]
            return jsonify(places)
        else:
            abort(404)
    elif request.method == 'POST':
        try:
            if not city:
                abort(404)
            place_data = request.get_json()
            if "user_id" not in place_data.keys():
                """
                -----------------------------------------------------
                Verify that in data user_id exist and that is correct
                -----------------------------------------------------
                """
                return jsonify("Missing user_id"), 400, {'ContentType':
                                                         'application/json'}
                user = storage.get(User, place_data["user_id"])
                if not user:
                    abort(404)
            if "name" not in place_data.keys():
                return jsonify("Missing name"), 400, {'ContentType':
                                                      'application/json'}
            else:
                new_place = Place(**place_data)
                # No sabemos si hay que guardar
                new_place.save()
                return jsonify(new_place.to_dict()), 201, {'ContentType':
                                                           'application/json'}
        except Exception:
            return jsonify("Not a JSON"), 400, {'ContentType':
                                                'application/json'}


@app_views.route("/places/<place_id>", methods=methods)
def places_by_id(place_id=None):
    """
    ----------------------
    Route for Place by id
    ----------------------
    """
    from models.place import Place
    from models.city import City
    from models.user import User
    from models import storage

    places = storage.all(Place)
    place = storage.get(Place, place_id)
    met = request.method
    if met in ["GET", "DELETE"]:
        res = aux_func(Place, met, place_id)
        return res
    elif met == "PUT":
        if place_id:
            key = "Place.{}".format(place_id)
            if key not in places.keys():
                abort(404)
            else:
                try:
                    data = request.get_json()
                    place = places[key]
                    for attr, value in data.items():
                        if attr not in ["id", "created_at", "updated_at",
                                        "user_id", "city_id"]:
                            setattr(place, attr, value)
                    # No sabemos si hay que guardar

                    storage.save()
                    return jsonify(place.to_dict()), 200, {'ContentType':
                                                           'application/json'}
                except Exception as err:
                    return jsonify("Not a JSON"), 400, {'ContentType':
                                                        'application/json'}
    else:
        abort(404)
