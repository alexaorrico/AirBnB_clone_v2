#!/usr/bin/python3
""" airbnb api wih flask"""


from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
CORS(app, resources={r"/api/v1*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearodwn_close(exception):
    """close data base"""
    storage.close()


@app.errorhandler(404)
@app.errorhandler(400)
def handle_request_error(exception):
    """Handle the request errors"""
    code = str(exception).split()[0]
    if code == '404':
        return make_response(jsonify({'error': "Not found"}), 404)
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
