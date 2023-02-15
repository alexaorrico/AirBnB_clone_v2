#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views
from flask import make_response


app = Flask(__name__)


app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True, debug=True)
