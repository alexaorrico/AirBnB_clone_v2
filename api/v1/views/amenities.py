#!/usr/bin/python3
<<<<<<< HEAD
"""amenities"""
=======
"""Amenity API"""
>>>>>>> 6c741cf84e75fc41aa58cd5e3aa2b5a541ea1aca
from api.v1.views import app_views
from flask import*
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def list_amenities():
    """list of amenities"""
    amen = storage.all(Amenity)
    return jsonify(
        [am.to_dict() for am in amen.values()]
    )



@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
<<<<<<< HEAD
    """id amenity"""
=======
    """Get amenity from storage"""
>>>>>>> 6c741cf84e75fc41aa58cd5e3aa2b5a541ea1aca
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
<<<<<<< HEAD
    """deleting amenity"""
=======
    """Delete amenity"""
>>>>>>> 6c741cf84e75fc41aa58cd5e3aa2b5a541ea1aca
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
<<<<<<< HEAD
    """create amenity"""
=======
    """Create an amenity"""
>>>>>>> 6c741cf84e75fc41aa58cd5e3aa2b5a541ea1aca
    get_json = request.get_json()
    if get_json is None:
        abort(404, 'Not a JSON')
    if get_json['name'] is None:
        abort(404, 'Missing Name')

    new_amenity = Amenity(**get_json)
    new_amenity.save()
    return jsonify(new_amenity.to_dict())



@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
<<<<<<< HEAD
    """update amenity"""
=======
    """Update Amenity"""
>>>>>>> 6c741cf84e75fc41aa58cd5e3aa2b5a541ea1aca
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort('404')
    if request.get_json() is None:
        abort('404', 'Not a JSON')
    update = request.get_json()
    for key, value in update.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
