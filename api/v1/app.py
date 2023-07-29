#!/usr/bin/python3

"""
create a variable app, instance of Flask
import storage from models
import app_views from api.v1.views
register the blueprint app_views to your Flask instance app
declare a method to handle @app.teardown_appcontext that calls storage.close()
inside if __name__ == "__main__":, run your Flask server (variable app) with:
host = environment variable HBNB_API_HOST or 0.0.0.0 if not defined
port = environment variable HBNB_API_PORT or 5000 if not defined
threaded=True
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown():
    """a method to handle @app.teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def handle_error(exception):
    """handles error in json format"""
    data = {
        "error": "Not found"
    }

    res = jsonify(data)
    res.status_code = 404

    return(res)


if __name__ == "__main__":
    app.run(getenv('HBNB_API_HOST'),getenv('HBNB_API_PORT'), threaded=True)
