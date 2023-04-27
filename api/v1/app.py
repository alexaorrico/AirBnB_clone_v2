#!/usr/bin/python3
""" Method that starts a Flask web application """
from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS
from flask import jsonify
from flask import make_response
from models import storage
import os

app = Flask(__name__)

#  To use any Flask Blueprint, you have
#  to import it and then register it in the application
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(self):
    """ this method logs out the database session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Error 404 """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(
            host=os.getenv("HBNB_API_HOST", '0.0.0.0'),
            port=os.getenv("HBNB_API_PORT", 5000),
            threaded=True,
            debug=True
           )
# app.config["DEBUG"] = True
