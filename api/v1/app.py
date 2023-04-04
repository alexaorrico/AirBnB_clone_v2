#!/usr/bin/python3
""" starting the Flash """
from views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv as env


# instance of flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://0.0.0.0:*"}})
# register blueprint
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """ 404(page not found) """
    code = error.__str__().split()[0]
    err_message = {"error": "Not Found"}
    return jsonify(code, err_message)


@app.teardown_appcontext
def teardown_db(exc):
    """ Close Storage """
    storage.close()


def start_flask():
    """ Start Flask """
    app.run(host=env('HBNB_API_HOST'),
            port=env('HBNB_API_PORT'),
            threaded=True)


if __name__ == '__main__':
    start_flask()
