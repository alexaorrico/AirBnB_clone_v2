#!/usr/bin/python3
''' Starts a flask session and imports blueprint '''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(self):
    ''' remove current storage sessions '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0' or HBNB_API_HOST,
            port='5000' or HBNB_API_PORT)
