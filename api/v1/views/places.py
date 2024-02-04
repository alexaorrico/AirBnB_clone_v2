#!/usr/bin/python3
"""
Update api/v1/views/places.py to add a new endpoint:
POST /api/v1/places_search
"""
from flask import Flask, request
from flask_restful import Resource, Api
from models import Place, State, City, Amenity

app = Flask(__name__)
api = Api(app)


class PlacesSearch(Resource):
    """PlacesSearch class"""

    def post(self):
        """post"""
        if not request.is_json:
            return {'message': 'Not a JSON'}, 400

        data = request.get_json()

        if not data or all(not data.get(key) for key in ['states', 'cities', 'amenities']):
            places = Place.query.all()
            return {'places': [place.serialize() for place in places]}

        query = Place.query

        if 'states' in data:
            state_ids = data['states']
            query = query.join(City).filter(City.state_id.in_(state_ids))

        if 'cities' in data:
            city_ids = data['cities']
            query = query.filter(Place.city_id.in_(city_ids))

        if 'amenities' in data:
            amenity_ids = data['amenities']
            query = query.join(Place.amenities).filter(Amenity.id.in_(amenity_ids))

        places = query.all()
        return {'places': [place.serialize() for place in places]}

api.add_resource(PlacesSearch, '/api/v1/places_search')

if __name__ == '__main__':
    """run the script"""
    app.run(debug=True)
