#!/usr/bin/python3
"""Flask App"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import json


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_appcontext(self):
    """Close storage"""
    storage.close()


@app.errorhandler(404)
def handle_404(e):
    """Error handler for 404 (Not Found) errors"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return make_response(response)


if __name__ == "__main__":
    """Main function"""
    from os import getenv
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
