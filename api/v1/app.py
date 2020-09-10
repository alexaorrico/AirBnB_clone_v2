#!/usr/bin/python3
""" Api Flask Run"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close(self):
    """ Calls storage.close """
    storage.close()


@app.errorhandler(404)
def json_404(error):
    """ Function to handle the 404 error - Not found """
    return jsonify({"error": "Not Found"})


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST") or "0.0.0.0",
            port=getenv("HBNB_API_PORT") or 5000, threaded=True)
