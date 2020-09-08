#!/usr/bin/python3
"""
    HBNB_V3: Task 9
"""
from api.v1.views.index import app_views, Amenity
from models import storage
from flask import jsonify, request, abort


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def viewalltheamenities():
    """AMEN ities"""

    if request.method == 'GET':
        atl = storage.all(Amenity)
        li = []
        for amen in atl.values():
            li.append(amen.to_dict())
        return jsonify(li)
    if request.method == 'POST':
        try:
            body = request.get_json()
            if "name" not in body.keys():
                abort(400, "Missing name")
            else:
                newamen = Amenity(**body)
                """for k in body.keys():
                    setattr(newstate, k, body.get(k))"""
                """newstate.__dict__.update(body)"""
                newamen.save()
                return jsonify(newamen.to_dict()), 201

        except:
            abort(400, "Not a JSON")


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def hailmary(amenity_id):
    """Handles an amenity object with said id depending on HTTP request"""
    atl = storage.all(Amenity)
    k = "Amenity." + amenity_id
    if k in atl.keys():
        a = atl.get(k)
        ad = a.to_dict()
        if request.method == 'GET':
            return jsonify(ad)
        if request.method == 'DELETE':
            storage.delete(a)
            storage.save()
            return jsonify({})
        if request.method == 'PUT':
            try:
                body = request.get_json()
                body.pop("id", "")
                body.pop("created_at", "")
                body.pop("updated_at", "")
                """s.__dict__.update(body)"""
                for k in body.keys():
                    setattr(a, k, body.get(k))
                """s.save()"""
                a.save()
                ad = a.to_dict()
                return jsonify(ad)

            except:
                abort(400, "Not a JSON")

    else:
        abort(404)
