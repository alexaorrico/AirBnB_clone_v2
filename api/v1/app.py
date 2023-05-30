#!/usr/bin/python3
''' Creates an instance of flask '''

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_d(self):
    ''' Tears down app.py '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    ''' Returns error 404'''
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    if os.getenv("HBNB_API_HOST") and os.getenv("HBNB_API_PORT"):
        app.run(host=os.getenv("HBNB_API_HOST"),
                port=os.getenv("HBNB_API_PORT"), threaded=True)
    else:
        app.run(host='0.0.0.0', port=5000, threaded=True)
