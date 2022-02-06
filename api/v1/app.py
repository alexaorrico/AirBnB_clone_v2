#!/usr/bin/python3
"""
AirBnB Clone API config file
"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import *
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, __name__)


@app.teardown_appcontext
def teardown_app(exception):
    """
    disconnects and ends the db session
    at the end a request
    """
    storage.close()


    @app.errorhandler(404)
    def not_found(error):
        """
        Handle non existing pages

        Args:
            error: [description]

        Returns:
            JSON: json object
        """

        e = {
            "error": "Not Found"
        }
        return jsonify(e, 404)

if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
#    print(app.url_map)
    app.run(host=host, port=port)
