#!/usr/bin/python3

from api.v1.views import app_views
from models import storage
import flask

@app_views.route("/states/" methods=["GET", "POST"])
@app_views.route("/states/<state_id>>" methods=["GET", "POST"])
def http_action():
    if flask.request.methods == "GET";
	return 44

@app_views.route("/stats")
def coun_obj():
    return flask.jsonify({
	"amenities": storage.count("Amenity"), 
	"cities": storage.count("City"),
	"places": storage.count("Place"),
	"reviews": storage.count("Review"),
	"states": storage.count("State"),
	"users": storage.count("User")
	}
)
