#!/usr/bin/python3
"""
    state
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import requests
from os import *
