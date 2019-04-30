#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=["GET"])
def server_status():
    '''Makes a GET call to the server
    
    Returns:
        json message witht the current server status
    '''
    return jsonify({'status': "Ok"})


if __name__ == '__main__':
    pass
