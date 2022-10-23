#!/usr/bib/python3
"""
Flask module to return the text as default route
"""
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_app(self):
    """close session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """handle page note found"""
    return make_response(jsonify(({"error": "Not found"}), 404))


if __name__ == "__main__":
    m = '0.0.0.0'
    if getenv('HBNB_API_HOST'):
        m = getenv('HBNB_API_HOST')
    p = '5000'
    if getenv('HBNB_API_PORT'):
        p = getenv('HBNB_API_PORT')
    app.run(debug=True, host=m, port=p, threaded=True)
