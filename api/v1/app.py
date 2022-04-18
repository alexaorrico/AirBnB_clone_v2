#!/usr/bin/python3
"""Flask app that intergrates with AirBnB static HTML Templates."""

from flask import Flask, jsonify, make_response, render_template, url_for
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException
import os
from flask_cors import CORS, cross_origin

#Global Flask App Variable
app = Flask(__name__)

#global strict slashes
app.url_map.strict_slashes = False

#flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

#Cross-Origin Resource Sharing
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

#app_views Blueprint defined in api.v1.views
app.register_blueprint(app_views)


#flask page rendering
@app.teardown_appcontext
def teardown():
    """after each request, this mtd calls .close()."""
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """handles 404page not found error."""
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


if __name__ == "__main__":
    app.run(host=host, port=port)
