#!/usr/bin/python3
"""
A Flask App that integrates with AirBnB static HTML Template
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
import os
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

#register the blueprint app_views to Flask instance app
app.register_blueprint(app_views)

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

@app.teardown_appcontext
def teardown_db(exception):
    """
    a method to handle @app.teardown_appcontext that calls storage.close()
    """
    storage.close()

def handle_exception(err):
    is_http_exception = isinstance(err, HTTPException)

    err_description = err.description if is_http_exception else str(err)
    code = err.code if is_http_exception else 500

    message = {'error': 'Not found' if is_http_exception and
            isinstance(err, NotFound) else err_description}

    return make_response(jsonify(message), code)

@app.errorhandler(Exception)
def global_error_handler(err):
    """
    Global Route to handle All Error Status Codes
    """
    return handle_exception(err)
    
if __name__ == "__main__":
    """
    MAIN Flask App starter
    """
    # start Flask app
    app.run(host=host, port=port, threaded=True))
