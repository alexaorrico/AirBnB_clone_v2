#!/usr/bin/python3
""" Flask web application API """
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views, state_view, place_view
from api.v1.views import reviews_view, city_view, user_view, amenities_view


app = Flask(__name__)
""" Flask web application instance """

app.register_blueprint(app_views)
app.register_blueprint(state_view)
app.register_blueprint(place_view)
app.register_blueprint(reviews_view)
app.register_blueprint(city_view)
app.register_blueprint(amenities_view)
app.register_blueprint(user_view)

@app.errorhandler(404)
def not_found_error(error):
    response = {
            "error": "Not found"
    }
    return jsonify(response), 404


@app.teardown_appcontext
def teardown_flask(exception):
    """ Flask request context listener """
    storage.close()


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=app_host, port=app_port, threaded=True)
