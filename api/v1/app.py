#!/usr/bin/python3

"""
creates a flask application
"""
from flask import Flask
from os import getenv

app = Flask(__name__)
from models import storage
from api.v1.views import app_views
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
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)
