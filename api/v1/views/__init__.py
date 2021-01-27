#!/usr/bin/python3
"""
Module for hbnb API api
"""
from flask import Flask, render_template, Blueprint, jsonify
app_views = Blueprint('app_views', '__name__', url_prefix='/api/v1')
from api.v1.views.index import *
