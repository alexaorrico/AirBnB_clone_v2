#!/usr/bin/python3
'''a script that starts a Flask web application has routes for
hbnb airBnB clone
'''

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_db(exception):
    '''Tear down seesion: db'''
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''Custom 404 error handler'''
    return make_response(jsonify({"error": "Not found"})), 404


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify(error.description)), 400


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
