#!/usr/bin/python3
"""App"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv as env


"""creating a instance of Flask & register blueprint"""
app = Flask(__name__)
app.register_blueprint(app_views)


# Handle teardown of app context
@app.teardown_appcontext
def teardown_context(exception):
    """ This method closes the storage session """
    storage.close()


# Define a route for the status of the API
@app.route('/api/v1/status', methods=['GET'])
def api_status():
    """ This method returns the status of the API """
    return jsonify(status="OK")


if __name__ == "__main__":
    # Run the Flask app
    host = env('HBNB_API_HOST', '0.0.0.0')
    port = int(env('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
