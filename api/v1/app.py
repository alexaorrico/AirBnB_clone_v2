#!/usr/bin/python3
"""app.py to connect to API"""
import storage from models
import app_views from api.v1.views
from flask import Flask
from flask import Blueprint


app = Flask('app')

#register the blueprint app_views to your Flask instance app
app_views = Blueprint("app", __name__)

#declare a method to handle @app.teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_appcontext:
    """teardown_appcontext"""
    storage.close()
def htmlNotFoundError():
    """htmlNotFoundError to handle HTML 404 Not Found errors"""
    return '{\n\t"error": "Not found"\n}'

if __name__ == "__main__":
    #run your Flask server (variable app) with:
    #host = environment variable HBNB_API_HOST or 0.0.0.0 as default value
    #port = environment variable HBNB_API_PORT or 5000 as default value
    app.run(host='0.0.0.0', port=5000)
