#!/usr/bin/python3
"""index.py to connect to API"""
import app_views from api.v1.views
hbnbClass = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
}

hbnbText = {
    "amenities",
    "cities",
    "places",
    "reviews",
    "states",
    "users"
}


@app_views.route('/status')
def hbnbStatus():
    """hbnbStatus"""
    return ('{\n\t"status": "OK"\n}')

@app_views.route('/api/v1/stats')
def hbnbStats():
    """hbnbStats"""
    numClass = len(hbnbText)
    str = '{\n\t"'
    for count in range(num):
        str += hbnbClass[count][0]
        str += "\": "
        str += str(storage.count(hbnbClass[count][0]))
        if count < numClass:
            str += ",\n"
    str += "\n}\n"
Footer

