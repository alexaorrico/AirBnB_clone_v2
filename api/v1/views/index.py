### TASK 5 nad STATUS ENDPOINT OF TASK 4 ###
#!/usr/bin/python3
"""Endpoints of the blueprint app_views"""
from flask import Flask, jsonify
from api.v1.views import app_views


@app.route('/status')
def api_status():
    """Endpoint (route) will be to return the status of the API"""
    # We can use json.dump() or flask.jsonify()
    return jsonify(status="OK")


@app.route('/stats')
def objects_qty():
    """Retrieves the number of each objects by type"""
    from models import storage
    return jsonify(
        amenities= storage.count("Amenity"),
        cities= storage.count("City"),
        places= storage.count("Place"),
        reviews= storage.count("Review"),
        states= storage.count("State"),
        users= storage.count("User")
    )


### TASK 6 ###
# check dependences: jsonify, ...

@app.errorhandler(404)
def page_not_found(error):
    """Handler for 404 errors that returns a JSON-formatted 404
    status code response"""
    return jsonify(error="Not found"), 404

### TASK 7 ###
# check dependences: jsonify, from models import State, abort, request, ...

@app.route('/api/v1/states', methods=["GET", "POST"]) # deberia sacarle el api/v1? ya estaria en el blueprint
def retrive_states():
    """Retrieves the list of all State objects"""
    if request.method == 'GET':
        all_states = []

        for obj in storage.all("State").values():
            all_states.append(obj.to_dict())

        return jsonify(all_states)

    elif request.method == 'POST':
        http_data = request.get_json()
        if not http_data:
            abort(404, 'Not a JSON')
        if "name" is not in http_data:
            abort(400, 'Missing name')
        
        new_state = State(**http_data)
        new_state.save()
        return new_state, 201


@app.route('/api/v1/states/<state_id>', methods=["GET", "DELETE", "PUT"]) # deberia sacarle el api/v1? ya estaria en el blueprint
def state_by_id(state_id):
    """Retrieves, deletes or updates a State object by state_id"""
    if request.method == 'GET':
        if state_id is not None:
            for obj in storage.all("State").values():
                if obj.id == state_id:
                    return jsonify(obj.to_dict())

    elif request.method == 'DELETE':
        if state_id is not None:
            for obj in storage.all("State").values():
                if obj.id == state_id:
                    storage.delete(obj)
                    storage.save()
                    return jsonify({}), 200

    elif request.method == 'PUT':
        if state_id is not None:
            for obj in storage.all("State").values():
                if obj.id == state_id:
                    http_data = request.get_json()
                    if not http_data:
                        abort(400, 'Not a JSON')

                    statics_attrs = ["id", "created_at", "updated_at"]
                    for key, value in http_data.items():
                        if key not in statics_attrs:
                            setattr(obj, key, value)
                    storage.save()
                    return jsonify(obj.to_dict()), 200                  
    else:
        abort(404)





