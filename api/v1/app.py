#!/usr/bin/python3
"""Flask app """
from api.v1.views import app_views
from flask import Flask, render_template, url_for
from models import storage
import os


app = Flask(__name__)
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """calls storage.close()"""
    storage.close()


if __name__ == "__main__":
    """runs flask"""
    app.run(host=host, port=port)

@app.errorhandler(404)
def handle_error404(exception):
    """returns a formated error page"""
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)
