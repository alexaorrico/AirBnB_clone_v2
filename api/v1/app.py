#!/usr/bin/python3
"""
creating an api
"""
from flask import Flask
from api.v1.views import app_views
from models import storage
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

api_host = getenv("HBNB_API_HOST", "0.0.0.0")
api_port = getenv("HBNB_API_PORT", 5000)

@app.teardown_appcontext
def teardown(self):
    """Deletes/removes instance of a session when done with it"""
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
	"""Load custom 404 page not found"""
	return make_response(jsonify({"error": "Not found"}), 404)

app.config['SWAGGER'] = {
	'title': 'AirBnB clone - RESTful API',
	'description': 'Api created for the hbnb restful api project,\
	all documentation shown below',
	'uiversion': 3}

Swagger(app)

if __name__ == "__main__":
    app.run(host=api_host, port=int(api_port), threaded=True)
