#!/usr/bin/python3
"""creates an instance of Flask"""
from Flask import Flask, make_response
from models import storage
from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)

@app.errorhandler(404)
def handle_404(exception):
    """handles 404 scenario (page not found)"""
    code = exception.__str__().split()[0]
    message = {"error": "Not found"}
    return make_response(message, code)


@app.teardown_appcontext
def teardowndb(exception):
    """close storage"""
    storage.close()


def start_flask():
    """start flask"""
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)

if __name__ == "__main__":
    start_flask()
