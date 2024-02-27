#!/usr/bin/python3
"""Main Flask application"""

from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


@app_views.errorhandler(404)
def not_found(error):
    """Handler for 404 errors."""
    return jsonify({"error": "Not found"}), 404


CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
