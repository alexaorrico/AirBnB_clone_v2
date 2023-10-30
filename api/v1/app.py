#!/usr/bin/python3

"""
implement status route
return the status of API
"""


from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


CORS(app, resources={r"/*": {"origins": "http://0.0.0.0"}})

@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors that returns a
    JSON-formatted 404 status code response"""
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.teardown_appcontext
def teardown(self):
    """
    close storage session
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
