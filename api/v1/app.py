#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask, jsonify, make_response, Blueprint
from models import storage
from api.v1.views import app_views
from os import environ
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
swagger = Swagger(app)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Close database connection after app context"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with a JSON response"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    """Main Function"""
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
