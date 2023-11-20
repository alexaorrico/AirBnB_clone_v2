#!/usr/bin/python3
""" Status of your API """
from flask import Flask, jsonify, make_response
from flask_cors import CORS
import os
from models import storage
from api.v1.views import app_views


@app.teardown_appcontext
def tear_it_down(stuff):
    """ close storage """
    storage.close()



if __name__ == '__main__':
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
