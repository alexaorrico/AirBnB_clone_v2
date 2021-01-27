#!/usr/bin/python3
"""Status of your API"""
from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from models import storage 
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_app(self):
    """" method that calls storage.close()"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", default="0.0.0.0"),
            port=getenv("BNB_API_PORT",default="5000"), 
            threaded=True)
