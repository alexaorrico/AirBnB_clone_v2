#!/usr/bin/python3
"""An app"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv

"""comment this out to use jsonify instead"""
import json
from flask import make_response
from json import dumps

app = Flask(__name__)
app.register_blueprint(app_views)


def jsonify(status=200, indent=4, sort_keys=True, **kwargs):
    """Comment this part out to return unformatted json response"""
    """Overwriting the jsonify function to return pretty output"""
    response = make_response(dumps(dict(**kwargs),
                                   indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response

@app.teardown_appcontext
def tear_all(exception=None):
    """A method that calls storage.close()
    Not specified in instruction but tear_all must have
    one argument, else TypeError"""
    storage.close()


@app.route('/api/v1/stats', strict_slashes=False)
def display_stats():
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    clss_stats = {}
    for key, value in classes.items():
        clss_stats[key] = storage.count(value)
    return jsonify(**clss_stats)
    """Should probably use jsonify instead of json.dumps but idk
    #return jsonify(clss_stats)
    #return str(storage.count(State))
    Using json.dumps for more readable output
    #return json.dumps(clss_stats, indent=4)"""


@app.errorhandler(404)
def handle_404(e):
    """Function to handle 404 error with a JSON formatted message"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=50000)

    app.run(host, port, threaded=True)
