#!/usr/bin/python3
<<<<<<< HEAD
"""Flask web application
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
=======
"""
starts a Flask web application
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_view)
>>>>>>> 7f463f781d2f2c16e360fbc7e590cd9adf4bcd7c


@app.teardown_appcontext
def teardown(error):
<<<<<<< HEAD
    """Clean-up method
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Custom 404 error
    """
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)
=======
    """ Close Storage """
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
>>>>>>> 7f463f781d2f2c16e360fbc7e590cd9adf4bcd7c
