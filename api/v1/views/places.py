'''Place Routes'''
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from . import app_views
from flask import make_response, abort, request


@app_views.get('cities/<city_id>/places')
def getPlaceByCity(city_id):
    '''Retrieves the list of all Place objects of a City'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = storage.all(Place)
    filtered_places = [place.to_dict()
                       for place in places.values() if place.city_id == city_id]
    return make_response(filtered_places)


@app_views.get('places/<place_id>')
def getPlace(place_id):
    '''Retrieves a Place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return make_response(place_id.to_dict())


@app_views.delete('places/<place_id>')
def deletePlace(place_id):
    '''Deletes a Place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response({})


@app_views.post('cities/<city_id>/places')
def createPlace(city_id):
    '''Creates a place'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if not data.get('user_id'):
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if not data.get('name'):
        abort(400, 'Missing name')
    place = Place(**data, city_id=city_id)
    place.save()
    return make_response(place.to_dict(), 201)


@app_views.put('places/<place_id>')
def updatePlace(place_id):
    '''Updates a place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    ignored = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for k, v in data.items():
        if k not in ignored:
            if k in place.__dict__:
                setattr(place, k, v)
    place.save()
    return make_response(place.to_dict())
