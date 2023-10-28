#!/usr/bin/python3
"""
Creation of a variable app(using flask)
"""


from flask import Flask, jsonify
from werkzeug.exceptions import NotFound
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def downtear(self):
    """A method to handle the app
    teardown"""
    storage.close()


@app.errorhandler(NotFound)
def not_found_error(e):
    '''return render_template'''
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
