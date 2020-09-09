#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 14:42:23 2020
@author: Robinson Montes
         Mauricio Olarte
"""
from flask import Blueprint
from . import *


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
