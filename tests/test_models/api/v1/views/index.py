# index.py

from flask import Flask, jsonify

app = Flask(__name__)

# Import views from api.v1
from api.v1.views import app_views

# Register the app_views blueprint
app.register_blueprint(app_views)

# Define a route /status that returns a JSON response
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Returns the number of each instance type """
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


