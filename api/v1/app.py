#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import Flask, make_response
from flask_cors import CORS
import json
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
host = getenv("HBNB_API_HOST")
port = getenv("HBNB_API_PORT")
cors = CORS(
    app,
    resources={r"/*": {"origins": "0.0.0.0"}}
    )


@app.teardown_appcontext
def teardown(err):
    """api teardown"""
    from models import storage

    storage.close()


@app.errorhandler(404)
def not_found(err):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    res = {'error': "Not found"}
    response = make_response(json.dumps(res), 404)
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == "__main__":
    """api entrypoint"""
    host = "0.0.0.0" if host is None else host
    port = "5000" if port is None else port
    app.run(host=host, port=port, threaded=True)

    from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

app = Flask(__name)

@app.errorhandler(404)
def handle_404_error(e):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)

