#!/usr/bin/python3

'''Building our AirBnB clone with RESTful API'''

if __name__ == "__main__":

    from flask import Flask, Blueprint, jsonify
    from flask_cors import CORS
    from models import storage
    from api.v1.views import app_views
    from os import getenv

    # Creating the Flask application
    app = Flask(__name__)
    app.register_blueprint(app_views)

    # CORS - Cross Origin Resource Sharing Configuration
    CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

    @app.teardown_appcontext
    def teardown(self):
        '''Closes the storage on teardown'''
        storage.close()

    @app.errorhandler(404)
    def page_not_found(exception):
        '''Handles 404 error'''
        return jsonify({"error": "Not found"}), 404

    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)
