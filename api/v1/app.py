#!/usr/bin/python3
"""Getting the API ready using flask blueprints"""
from flask import Flask, url_for, jsonify, make_response, render_template
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Register blueprint
app.register_blueprint(app_views)

# Enviromental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 500)
app.threaded = True


@app.teardown_appcontext
def teardown_db(exception):
    """Invokes the storage close method of the current session"""
    storage.close()


@app.errorhandler(Exception)
def global_error_handler(err):
    """Error Handler """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


if __name__ == "__main__":
    """Runs only if main"""
    app.run(host=host, port=port, debug=True)
