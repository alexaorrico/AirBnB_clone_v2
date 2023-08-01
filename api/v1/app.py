#!/usr/bin/python3
"""Returns the status of the API"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import make_response
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)
app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def storage_close(value):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """return page not found error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST', default='0.0.0.0')
    HBNB_API_PORT = getenv('HBNB_API_PORT', default=5000)
    app.run(host=HBNB_MYSQL_HOST, port=int(HBNB_API_PORT), threaded=True)
