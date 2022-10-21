#!/usr/bin/python3
""" an api """


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(x):
    """closes the current db transaction"""
    storage.close()


def handle_404(x):
    """ returns json formatted error message """
    return jsonify({
            "error": "Not found"
        }), 404


app.register_error_handler(404, handle_404)


if __name__ == "__main__":
    import os
    host = os.getenv("HBNB_API_HOST")
    if not host:
        host = "0.0.0.0"
    port = os.getenv("HBNB_API_PORT")
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True, debug=True)
