#!/usr/bin/python3
""" module api """
from flask import Flask, jsonify, make_response
from werkzeug.exceptions import NotFound
from models import storage
from api.v1.views import app_views
from flask import Blueprint
from flask_cors import CORS, cross_origin
app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views) #register blue print

@app.teardown_appcontext
def tear_down():
    """ to close a calls """
    storage.close()
    
@app.errorhandler(404)
def error_handler(error):
    """ handle 404 errors """
    return make_response(jsonify({"error": "Not found"}), 404)
    

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    
    app.run(host=host, port=port, thread=True)
