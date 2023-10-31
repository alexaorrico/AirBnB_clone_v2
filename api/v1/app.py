#!/usr/bin/python3
<<<<<<< HEAD
"""app"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
=======
"""
Script uses blueprint object for routing the application
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import environ
>>>>>>> 206a6e57f538ad1f84b5eb5219200406d63cb1c7
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
<<<<<<< HEAD
=======


app.url_map.strict_slashes = False
app.register_blueprint(app_views)
>>>>>>> 206a6e57f538ad1f84b5eb5219200406d63cb1c7

app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.teardown_appcontext
<<<<<<< HEAD
def close_storage(self):
    '''Closes the storage engine'''
    storage.close()

if __name__ == '__main__':
    api_host = getenv("HBNB_API_HOST", '0.0.0.0')
    api_port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=api_host, port=api_port, threaded=True)
=======
def teardown_db(error):
    """
    function closes the db when called
    """
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """
    404 error handler
    """
    return make_response(jsonify({"error": 'Not found'}), 404)


if __name__ == '__main__':
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')

    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000

    app.run(host=host, port=port, threaded=True)  # type: ignore
>>>>>>> 206a6e57f538ad1f84b5eb5219200406d63cb1c7
