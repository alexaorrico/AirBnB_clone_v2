#!/usr/bin/python3
"""
controller that execute the app
and assemble the components -> blueprints
"""
from flask import Flask, jsonify
import werkzeug.exceptions
import werkzeug
from os import environ, getenv
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app=app, resources={r"/*": {'origins': '0.0.0.0'}})


if __name__ == "__main__":
    from api.v1.views import app_views

    @app_views.errorhandler(werkzeug.exceptions.NotFound)
    def page_not_found(error):
        """handle error page"""
        return jsonify({"error": "Not found"}), 404

    app.register_blueprint(app_views)
    app.register_error_handler(404, page_not_found)

    @app.teardown_appcontext
    def teardown(exception=None):
        """tear down that close the storage engine"""
        from models import storage
        storage.close()

    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if host is None:
        host = "0.0.0.0"
    if port is None:
        port = 5000
    app.run(host=host, port=port, threaded=True)
