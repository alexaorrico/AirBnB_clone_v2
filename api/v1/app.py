#!/usr/bin/python3
"""app.py"""
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException
from flask import Flask
from os import getenv
from flask import jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={"/*": {"origins": '0.0.0.0'}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_appcontext(error):
    """teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def page_404(error):
    """ Return a custom 404 error """
    err_dict = {"error": "Not found"}
    return jsonify(err_dict), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
