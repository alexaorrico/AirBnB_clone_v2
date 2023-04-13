#!/usr/bin/python3
"""INDEX.PY

    Route Status
"""


from flask import jsonify
from api.v1.app import app

@app.route('/status', strict_slashes=False)
def index():
    """
     Return status of API.
     Used to check if user is allowed to access API
     
     @return jsonified version of status
    """
    return jsonify({"status": "OK"})


@app.route('/stats', strict_slashes=False)
def count():
    """
     Count how many records exist in the database.
     This is useful for determining if a query is valid or not.
     
     @return 200 if everything worked 400 if something went wrong with the
    """
    return jsonify({"status": "OK"})
