#!/usr/bin/python3
"""
Test .get() and .count() methods 
Test .get() and .count() methods
"""
import os
from sqlalchemy import create_engine
from models import storage
from models.state import State

# Get the environment variables
user = os.environ.get('HBNB_MYSQL_USER')
password = os.environ.get('HBNB_MYSQL_PWD')
host = os.environ.get('HBNB_MYSQL_HOST')
database = os.environ.get('HBNB_MYSQL_DB')

# Create the SQLAlchemy engine
engine = create_engine('mysql://' + user + ':' + password + '@' + host + '/' + database)

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))
