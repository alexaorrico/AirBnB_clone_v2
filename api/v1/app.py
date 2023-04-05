#!/usr/bin/python3
""" instance of Flask """
from flask import Flask, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv as env


# create an instance of Flask
app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
# register blueprint
app.register_blueprint(app_views)


@app.errorhandler(404)
def handle_404(exception):
    """handles 404 scenario (page not found)"""
    code = exception.__str__().split()[0]
    message = {"error": "Not found"}
    return make_response(message, code)


@app.teardown_appcontext
def teardown_db(exception):
    """ close storage """
    storage.close()


def start_flask():
    """ start flask """
    app.run(host=env('HBNB_API_HOST'),
            port=env('HBNB_API_PORT'),
            threaded=True)


if __name__ == "__main__":
    start_flask()
