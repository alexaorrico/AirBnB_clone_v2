#!/usr/bin/python3

from api.v1.views import app_views


@app_views.route('/status')
def status():
    """api status ok"""
    return {'status': 'OK'}


@app_views.route('/stats')
def number_objects():
    """counts objects in DB"""
    from models import storage
    from console import classes
    from console import BaseModel
    new_dict = {}

    for class_found in classes.values():
        if class_found != BaseModel:
            new_dict[class_found.__tablename__] = storage.count(
                class_found)
    return new_dict
