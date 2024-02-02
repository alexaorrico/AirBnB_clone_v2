#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views
from storage import count

# Define route for index
@app_views.route('/', methods=['GET'])
def index():
    return jsonify(message='Welcome to the API!')

# Define route for status
@app_views.route('/status', methods=['GET'])
def status():
    return jsonify(status='OK')

stats_blueprint = Blueprint('stats', __name__)

@stats_blueprint.route('/api/v1/stats', methods=['GET'])
def get_stats():
    # Call the count() method from storage to retrieve the number of each object by type
    object_counts = count()

    # Return the counts as a JSON response
    return jsonify(object_counts)
