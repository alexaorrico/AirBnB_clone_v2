#!/usr/bin/python3
<<<<<<< HEAD
"""app.py to connect to API"""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
=======
"""
    app for registering blueprint and starting flask
"""
from os import getenv


from api.v1.views import app_views
from flask import Flask, jsonify, make_response
>>>>>>> f61419b9c8d53faeeaab2f7b00854c945df71058
from flask_cors import CORS
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
<<<<<<< HEAD
def teardown_appcontext(code):
    """teardown_appcontext"""
=======
def tear_down(self):
    """closes storage after each session"""
>>>>>>> f61419b9c8d53faeeaab2f7b00854c945df71058
    storage.close()


@app.errorhandler(404)
<<<<<<< HEAD
def page_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
=======
def not_found(error):
    '''
    return JSON formatted 404 status code response
    '''
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
>>>>>>> f61419b9c8d53faeeaab2f7b00854c945df71058
