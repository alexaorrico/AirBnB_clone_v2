#!/usr/bin/python3
"""
Creates a new view for User objects for all default API actions
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.user import User


def getuser(user):
    """Get user"""
    return (user.to_dict(), 200)


def putuser(user):
    """Update user """
    if not request.is_json:
        abort(400, "Not a JSON")
    new = request.get_json()
    for (k, v) in new.items():
        if k is not 'id' and k is not 'email'\
           and k is not 'created_at' and k is not 'updated_at':
            setattr(user, k, v)
    storage.save()
    return (user.to_dict(), 200)


def deleteuser(user):
    """Delete user """
    storage.delete(user)
    storage.save()
    return ({}, 200)


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """  Retrieves list of all user or creates an useer """
    if request.method == 'GET':
        all_users = [x.to_dict() for x in storage.all('User').values()]
        return (jsonify(all_users), 200)
    elif request.method == 'POST':
        if not request.is_json:
            abort(400, "Not a JSON")
        new = request.get_json()
        if 'email' not in new.keys():
            abort(400, "Missing email")
        if 'password' not in new.keys():
            abort(400, "Missing password")
        x = User()
        for (k, v) in new.items():
            setattr(x, k, v)
        x.save()
        return (x.to_dict(), 201)


@app_views.route('/users/<ident>', methods=['GET', 'PUT', 'DELETE'])
def users_id(ident):
    """Retrieves a user object"""
    users = storage.all('User')
    for s in users.values():
        if s.id == ident:
            if request.method == 'GET':
                return getuser(s)
            elif request.method == 'PUT':
                return putuser(s)
            elif request.method == 'DELETE':
                return deleteuser(s)
    abort(404, 'Not found')
