#!/usr/bin/python3
""" Api module """
from api.v1.views import app_views
from flask import Flask
from models import storage
import os

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """teardown"""
    storage.close()

# Defines a custom 404 error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    env_host = 'HBNB_API_HOST'
    env_port = 'HBNB_API_PORT'
    host = os.getenv(env_host, default='0.0.0.0')
    port = os.getenv(env_port, default=5000)
    app.run(host=host, port=port, threaded=True)
