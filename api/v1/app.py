#!/usr/bin/python3
"""App module
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_db(error):
    """Closes the database again at the end of the request.
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ handler for 404 errors that returns a
        JSON-formatted 404 status code
    """
    err_stat = {"error": "Not found"}
    return jsonify(err_stat), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host, port, threaded=True)
