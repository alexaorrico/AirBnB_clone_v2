#!/usr/bin/python3

"""
starts a Flask web application
"""

from os import getenv
from flask import Flask
from models import storage
from api.v1.views.index import app_views
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(e):
    """error 404 handler"""
    return {"error": "Not found"}, 404


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':

    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)
