 #!/usr/bin/python3
"""Beginning of the index"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.base_model import BaseModel
from models.user import User

@app_views.route('/status, method=[GET]')
def status():
    """return JSON status:OK

    Returns:
        _type_: _description_
    """
    return jsonify(status= 'OK')

@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Retrieves the number of each object by type.
    """
    classes = {"base_model": "BaseModel", "user": "User"}
    # Add other classes as needed
    for key in classes:
        classes[key] = storage.count(eval(classes[key]))
    return jsonify(classes)
