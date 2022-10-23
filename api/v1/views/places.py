"""Module users.py: contains users information"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place(place_id):
    """returns an place based on it's id"""
    for place in storage.all(Place).values():
        print(place)
        if place.id == place_id:
            print('yes')
            if request.method == 'DELETE':
                place.delete()
                storage.save()
                return '{}'

            if request.method == 'PUT':
                res = request.get_json()
                print(res)
                if res is None:
                    abort(400, description='Not a JSON')
                for k, v in res.items():
                    if k.endswith('ed_at') or k.endswith('id'):
                        continue
                    setattr(place, k, v)
                place.save()

            return jsonify(place.to_dict())

    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """displays and creates an place"""
    if request.method == 'POST':
        res = request.get_json()
        print(res)
        if res is None:
            abort(400, description='Not a JSON')
        if 'name' not in res.keys():
            abort(400, description='Missing name')

        if 'user_id' not in res.keys():
            abort(400, description='Missing user_id')

        users = [user.id for user in storage.all(User).values()]
        if res['user_id'] not in users:
            abort(404)

        for city in storage.all(City).values():
            if city_id == city.id:
                res['city_id'] = city.id
                new_place = Place(**res)
                new_place.save()
                return jsonify(new_place.to_dict()), 201

        abort(404)

    place = [v.to_dict() for v in storage.all(Place).values()]
    return jsonify(place)