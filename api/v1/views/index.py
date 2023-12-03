#!/usr/bin/python3

"""

solution for task 3(index.py):

"""

from api.v1.views import app_views

from flask import Flask, jsonify



@app_views.route('/status', strict_slashes=False)



def get_status():

	"""

     we are going to just document this

	"""

    return jsonify({"status": "OK"})
