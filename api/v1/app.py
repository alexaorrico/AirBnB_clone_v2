#!flask/bin/python3
"""Flask app module"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(exception):
    """Close storage when app context tears down"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return response for error 404"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    import os
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
