#!/usr/bin/python3
"""
    HBNB_V3: Task 11 and 16
"""
from api.v1.views.index import app_views, Place, User, City, State
from models import storage
from flask import jsonify, request, abort, make_response


@app_views.route('/places_search',
                 methods=['POST'], strict_slashes=False)
def viewalltheplacethingswithsearchyo():
    """ read the method name, duh """
    if request.method == 'POST':
        try:
            body = request.get_json()
            k = body.keys()
        except:
            return "Not a JSON", 400
        li = []
        if "states" in body.keys():
            sts = body.get('states')
            states = storage.all(State)
            for st in states.values():
                if st.__dict__['id'] in sts:
                    for cty in st.cities:
                        for plc in cty.places:
                            if plc not in li:
                                li.append(plc)
        if "cities" in body.keys():
            cties = body.get('cities')
            cities = storage.all(City)
            for cty in cities.values():
                if cty.__dict__['id'] in cties:
                    for plc in cty.places:
                        if plc not in li:
                            li.append(plc)
        if "amenities" in body.keys():
            for plc in li.copy():
                for amty in body.get("amenities"):
                    actual = storage.get(Amenity, amty)
                    if actual not in plc.amenities:
                        li.pop(plc)
        newli = []
        for plc in li:
            newli.append(plc.to_dict())
        return jsonify(newli)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def viewalltheplacethings(city_id):
    """Retrieves the list of all State objects"""
    if storage.get(City, city_id) is None:
        abort(404)
    if request.method == 'GET':
        cty = storage.get(City, city_id)
        ptl = cty.places
        places = [place.to_dict() for place in ptl]
        return jsonify(places)
    if request.method == 'POST':
        try:
            body = request.get_json()
            if "user_id" not in body.keys():
                return "Missing user_id", 400
            elif "name" not in body.keys():
                return "Missing name", 400
            else:
                if storage.get(User, body.get('user_id')) is None:
                    return "", 404
                body.update({"city_id": city_id})
                newplace = Place(**body)
                """for k in body.keys():
                    setattr(newstate, k, body.get(k))"""
                """newstate.__dict__.update(body)"""
                newplace.save()
                return jsonify(newplace.to_dict()), 201
        except:
            return "Not a JSON", 400


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def placeidtime(place_id):
    """Handles a state object with said id depending on HTTP request"""
    ptl = storage.get(Place, place_id)
    if ptl is not None:
        sd = ptl.to_dict()
        if request.method == 'GET':
            return jsonify(sd)
        if request.method == 'DELETE':
            storage.delete(ptl)
            storage.save()
            return jsonify({})
        if request.method == 'PUT':
            try:
                body = request.get_json()
                body.pop("id", "")
                body.pop("created_at", "")
                body.pop("updated_at", "")
                body.pop("user_id", "")
                body.pop("city_id", "")
                """s.__dict__.update(body)"""
                for k in body.keys():
                    setattr(ptl, k, body.get(k))
                """s.save()"""
                ptl.save()
                sd = ptl.to_dict()
                return jsonify(sd)
            except:
                return "Not a JSON", 400

    else:
        abort(404)
