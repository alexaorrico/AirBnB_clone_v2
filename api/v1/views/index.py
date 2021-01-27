#!/usr/bin/python3
"""
Module for hbnb API api
"""
from flask import Flask, render_template, Blueprint, jsonify
from api.v1.views from app_views
from models import storage


@app.route('/status/', strict_slashes=False)
def status():
    nominal = jsonify({"Status": "OK"})
    return nominal
