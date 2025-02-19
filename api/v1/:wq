#!/usr/bin/python3
"""my app"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """method to closes storage engine"""
    storage.close()


@app.errorhandler(404)
def err404(error):
    error404 = {'error': 'Not found'}
    return make_response(jsonify(error404), 404)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
