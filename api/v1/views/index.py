#!/usr/bin/python3
'''index page for the status of api'''


from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models.engine import count, db_storage


@app_views.route('/status', strict_slashes=False)
def status():
    '''return status'''
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats')
def stats():
    my_list = {}
    for stats in db_storage.classes:
        num = db_storage.count(stats)
        my_list.update({'stats': num})
    return jsonify({my_list})


if __name__ == "__main__":
    pass
