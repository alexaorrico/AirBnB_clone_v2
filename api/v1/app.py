#!/usr/bin/python3
"""my app"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """handle @app.teardown_appcontext that calls close()"""
    storage.close()

@app.errorhandler(404)
def err404(error):
    """handler for 404 errors that returns a JSON-formatted 404 status"""
    error404 = {'error': 'Not found'}
    return make_response(jsonify(error404), 404)

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
