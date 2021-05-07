#!/usr/bin/python3
""" Status json """
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def return_json():
    """ Return a json status """
    return '{\n  "status": "OK"\n}\n'


@app_views.route('/stats')
def return_stats():
    """ To get the number of objects by type """
    obj_classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }

    json_objs = ''
    json_objs += ("{\n")

    for key, value in obj_classes.items():
        count_obj = storage.count(value)
        str_obj = '  \"' + key + '\"' + ': ' + "{}".format(count_obj)
        json_objs += str_obj

        if key != 'users':
            json_objs += ',\n'

    json_objs += '\n}\n'

    return(json_objs)
