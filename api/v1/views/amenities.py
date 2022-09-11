#!/usr/bin/python3
"""
-----------------------
New view for Amenities
-----------------------
"""


from flask import jsonify, request, abort
from api.v1.views import app_views

methods = ["GET", "DELETE", "POST", "PUT"]


@app_views.route("/amenities", methods=methods)
@app_views.route("/amenities/<amenity_id>", methods=methods)
def amenities(amenity_id=None):
    """
    --------------------
    Route for Amenities
    --------------------
    """
    from models.amenity import Amenity
    from models import storage
    from api.v1.views.aux_func import aux_func

    amenities = storage.all(Amenity)
    met = request.method
    if met in ["GET", "DELETE"]:
        # Auxiliar func to requests methods
        res = aux_func(Amenity, met, amenity_id)
    elif met == "POST":
        try:
            data = request.get_json()
            if "name" not in data.keys():
                return jsonify("Missing name"), 400, {'Content-Type':
                                                      'application/json'}
            else:
                new_amenity = Amenity(**data)
                # No sabemos si hay que guardar
                new_amenity.save()
                return jsonify(new_amenity.to_dict()), 201, {
                    'Content-Type': 'application/json'}
        except Exception as err:
            return jsonify("Not a JSON"), 400, {'Content-Type':
                                                'application/json'}
    elif met == "PUT":
        if amenity_id:
            key = "Amenity.{}".format(amenity_id)
            if key not in amenities.keys():
                abort(404)
            else:
                try:
                    data = request.get_json()
                    amenity = amenities[key]
                    for attr, value in data.items():
                        if attr not in ["id", "created_at", "updated_at"]:
                            setattr(amenity, attr, value)
                    # No sabemos si hay que guardar
                    storage.save()
                    return jsonify(amenity.to_dict()), 200, {
                        'Content-Type': 'application/json'}
                except Exception as err:
                    return jsonify("Not a JSON"), 400, {'Content-Type':
                                                        'application/json'}
    return res
