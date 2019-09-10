#!/usr/bin/python3
''' py file to connect to API  '''
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origin": "0.0.0.0"}})

@app.teardown_appcontext
def teardown_appcontext(code):
    'closes storage method'
    storage.close()

if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')))
