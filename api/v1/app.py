#!/usr/bin/python3
"""
<<<<<<< HEAD
This module contains the principal application
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(obj):
    """ calls methods close() """
    storage.close()


@app.errorhandler(404)
def page_not_foun(error):
    """ Loads a custom 404 page not found """
    return make_response(jsonify({"error": "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB clone - RESTful API',
    'description': 'This is the api that was created for the hbnb restful api project,\
    all the documentation will be shown below',
    'uiversion': 3}

Swagger(app)

if __name__ == "__main__":

    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host, int(port), threaded=True)
=======
module to start using api
"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.teardown_appcontext
def exit(exception):
    ''' exit api in case of unexpected error '''
    storage.close()

@app.errorhandler(404)
def error404(e):
    """ instance of app to handle 404 errors """
        response = {"error": "Not found"}
        return make_response(jsonify(response), 404)

    if __name__ == '__main__':
        host = getenv("HBNB_API_HOST")
        port = getenv("HBNB_API_PORT")
        if host is None:
            host = '0.0.0.0'
        if port is None:
            port = 5000
        app.run(host=host, port=port)
>>>>>>> master
