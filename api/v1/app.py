#!/usr/bin/python3
"""Flask application"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_storage(self):
    """Teardown method that close session of database"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """handler for 404 errors """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST", default="0.0.0.0"),
            port=getenv("HBNB_API_PORT", default="5000"), threaded=True)
