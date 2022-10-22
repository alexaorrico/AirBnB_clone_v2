#!/usr/bin/python3
""" an api """


from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from api.v1.views import state_views
from api.v1.views import city_views
from api.v1.views import amenity_views
from api.v1.views import user_views
from api.v1.views import place_views
from api.v1.views import review_views


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.register_blueprint(state_views)
app.register_blueprint(city_views)
app.register_blueprint(amenity_views)
app.register_blueprint(user_views)
app.register_blueprint(place_views)
app.register_blueprint(review_views)


@app.teardown_appcontext
def close_session(x):
    """closes the current db transaction"""
    storage.close()


def handle_404(x):
    """ returns json formatted error message """
    return jsonify({
            "error": "Not found"
        }), 404


app.register_error_handler(404, handle_404)


if __name__ == "__main__":
    import os
    host = os.getenv("HBNB_API_HOST")
    if not host:
        host = "0.0.0.0"
    port = os.getenv("HBNB_API_PORT")
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True, debug=True)
