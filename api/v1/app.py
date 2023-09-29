#!/usr/bin/python3
"""first endpoint (route) will be to return the status of your API"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import Flask, jsonify, make_response, render_template, url_for


app = Flask(__name__)

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)


# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)



@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    """Start flask app"""
    app.run(host=host, port=port, threaded=True)
