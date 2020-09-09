#!/usr/bin/python3
"""API Status"""
<<<<<<< HEAD
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
=======
from flask import Flask
from models import storage
from api.v1.views import app_views
>>>>>>> a659d09f58510d3bc575fc2d7842ee02c701c550

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def CloseSession(self):
    """Close session"""
    storage.close()

<<<<<<< HEAD

@app.errorhandler(404)
def error_404(error):
    """Error 404 handler"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', 5000)), threaded=True)
=======
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
>>>>>>> a659d09f58510d3bc575fc2d7842ee02c701c550
