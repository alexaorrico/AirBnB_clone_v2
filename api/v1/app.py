#!/usr/bin/python3

'''Building our AirBnB clone with RESTful API'''

if __name__ == "__main__":

    from flask import Flask, Blueprint, jsonify
    from models import storage
    from api.v1.views import app_views
    from os import getenv

    # Creating the Flask application
    app = Flask(__name__)
    app.register_blueprint(app_views)

    @app.teardown_appcontext
    def teardown(self):
        '''Closes the storage on teardown'''
        storage.close()

    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)
