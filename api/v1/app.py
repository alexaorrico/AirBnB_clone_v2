#!/usr/bin/python3
'''Flask server app var'''
from models import storage
from os import getenv
from flask import Flask, jsonify
from api.v1.views import app_views
from flask_cors import CORS

# Create a variable app, instance from flask
app = Flask(__name__)
# Managing CORS (Cross Origin Resource Sharing)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
# For a better identation of JSON response
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# register the blueprint app_views to your app
app.register_blueprint(app_views)
# disables this strict trailing slash behavior.
app.url_map.strict_slashes = False


# method to handle the close of the app
@app.teardown_appcontext
def down_method(self):
    """ close the storage"""
    storage.close()


# Function to handle 404 error
@app.errorhandler(404)
def page_not_found(e):
    """ Method to handle
    the error page
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'
    if getenv('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    else:
        port = 5000
    app.run(host=host, port=port, threaded=True)
