#!/usr/bin/python3

from flask import Flask, jsonify, request, make_response
from api.v1.views import app_views
from models.amenity import Amenity
from flask import abort
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app_views.route('/amenities', methods=['GET'])
def getAllamenity():
    """get all amenities"""
    amenities = []
    all = storage.all("Amenity").values()
    for x in all:
        amenities.append(x.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'])
def getByIdamenity(amenity_id):
    amenities = storage.get("Amenity", amenity_id)
    if amenities is None:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def deleteByIdamenity(amenity_id):
    """ delete by id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({})


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """"""
    name = 'name'
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if name not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    data = request.get_json()
    amenity = Amenity()

    amenity.name = data['name']

    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()

    amenity.name = data['name']
    amenity.save()
    return jsonify(amenity.to_dict())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
