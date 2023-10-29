#!/usr/bin/python3
'''endpoint (route) will be to return the status of your API'''

from flask_cors import CORS
from api.v1.views import app_views
from flask import Flask, jsonify
import os
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/v1/*": {"origins": "https://0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    ''' calls storage.close() '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True, debug=True)
