#!/usr/bin/python3
"""An API to retrieve States data"""
from api.v1.views import app_views
from flask import abort, Response
import json
import models
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """Retrieves all state objects"""
    state_objects = models.storage.all(State).values()
    states = [items.to_dict() for items in state_objects]
    return Response(json.dumps(states, indent=2),
                    mimetype='application/json')


@app_views.route('/states/<int:id>', methods=['GET'])
def get_state(id):
    """Retrieves a state according to the id passed"""
    state_objects = models.storage.all(State).values()
    for items in state_objects:
        if items.id == id:
            state = items
    if state is None:
        abort(404)
    return Response(json.dumps((state.to_dict()), indent=2),
                    mimetype='application/json')
