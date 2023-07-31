#!/usr/bin/python3

""" Flask Application """
from flask import Flask
from api.v1.views import app_views
from models import storage

# Create a Flask app instance
app = Flask(__name__)

# Register the app_views blueprint with the Flask app
app.register_blueprint(app_views, url_prefix='/api/v1')

# Teardown app context to close the database session after each request
@app.teardown_appcontext
def teardown_app_context(exception):
    storage.close()

# Only run the app if this file is executed directly, not imported as a module
if __name__ == "__main__":
    # Get the host and port from environment variables or use default values
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5000"))

    # Run the Flask app
    app.run(host=host, port=port, threaded=True)

"""The app thet contains the principal application """
from api.v1.views import app_views
from models import storage
from flask import Flask, make_response, jsonify
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app, origin="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """ close query after each session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Loads a custom 404 page not found """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_HOST', default=5000)

    app.run(host, int(port), threaded=True)
