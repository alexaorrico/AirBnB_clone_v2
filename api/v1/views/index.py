#usr/bin/env python
"""Beginning of the index"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status, method=[GET]')
def status():
    """return JSON status:OK

    Returns:
        _type_: _description_
    """
    return jsonify(status= 'OK')
