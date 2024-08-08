#!/usr/bin/python3
""" Test .get()
"""
from models import storage
from models.state import State


def wrapper_all_type(m_class):
    res = {}
    try:
        res = storage.all(m_class)
    except:
        res = {}
    if res is None or len(res.keys()) == 0:
        try:
            res = storage.all(m_class.__name__)
        except:
            res = {}
    return res

state_ids = []
state_ids_found = []
for state in wrapper_all_type(State).values():
    state_ids.append(state.id)

if len(state_ids) == 0:
    print("empty", end="")
else:
    for state_id in state_ids:
        state = storage.get(State, state_id)
        if state is not None and state.id == state_id:
            state_ids_found.append(state_id)
    
    if len(state_ids_found) != len(state_ids):
        # try with `<class_name>.<id>`
        state_ids = wrapper_all_type(State).keys()
        state_ids_found = []
        for state_id in state_ids:
            state = storage.get(State, state_id)
            if state is not None and state.id == state_id:
                state_ids_found.append(state_id)
    
    if len(state_ids_found) == len(state_ids):
        print("Get success", end="")
    else:
        print("Get doesn't retreive all State in storage", end="")
