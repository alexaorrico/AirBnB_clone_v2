#!/usr/bin/pyhton3
"""Views for States"""

form api.v1.views import app_views
from models import storage


@app_views.route('/api/v1/states/<state.id>',
                 method=['GET', 'POST'], strict_slashes=False)
def states():
	if state.id:
	    all_states = storage.all(State).to_dict()

		for stte in all_states:
		    if stte.id == state.id
	else:
		
