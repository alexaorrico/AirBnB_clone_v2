#!/usr/bin/python3
<<<<<<< HEAD
"""starting a Flask application"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

@app.teardown_appcontext
def storage_close(Exception):
    """Closes storage"""
    storage.close()

if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
=======
""" Flask app for aibrnb clone"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(exception):
    """closes current sqlalchemy session"""
    storage.close()


host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', '5000')


if __name__ == "__main__":
    """Main function for flask app"""
>>>>>>> 6338784aeb158049a5574267bcaba8774a776573
    app.run(host=host, port=port, threaded=True)
