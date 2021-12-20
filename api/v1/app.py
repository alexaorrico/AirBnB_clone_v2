#!/usr/bin/python3
'''sets up Flask app'''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

# Start Flask app
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(context):
    """reloads storage after each request"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """404 response"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    """
    run the app host
        defaults:
            host='0.0.0.0'
            port='5000'
    """
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = getenv("HBNB_API_PORT", '5000')
    app.run(host=host, port=port, threaded=True)
