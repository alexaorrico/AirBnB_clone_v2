#!/usr/bin/python3
"""Flask instance startup"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Stops instance"""
    storage.close()


@app.errorhandler(404)
def handle_404_error(error):
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response

if __name__ == "__main__":
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
