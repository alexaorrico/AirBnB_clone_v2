#!/usr/bin/python3

"""
creates a flask application
"""
from flask import Flask
from os import getenv
from flask import make_respons
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown():
    """a method to handle @app.teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def handle_error(error):
    """handles error in json format"""
    error_mesg = {
        "error": "Not found"
    }

    return make_response(jsonify(error_mesg), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)
