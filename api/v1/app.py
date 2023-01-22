from os import getenv
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views

app = Flask('__name__')

app.register_blueprint(app_views)
app.url_map.strict_slashes = False

@app.teardown_appcontext
def teardown_app(exception):
    """ends a db session at the end of a request"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """a handler for 404 errors that returns a JSON-formatted
    404 status code response
    """
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port)
