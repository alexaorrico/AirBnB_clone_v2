#!/usr/bin/python3
"""
script to get, update, create and delete a user
"""
from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
