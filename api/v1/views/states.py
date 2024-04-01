#!/usr/bin/python3
"""An API to retrieve States data"""
from api.v1.views import app_views
from flask import abort, Response, jsonify, request
import models
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states() -> Response:
    """Retrieves all state objects"""
    state_objects = models.storage.all(State).values()
    states = [items.to_dict() for items in state_objects]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id) -> Response:
    """Retrieves a state according to the state_id passed"""
    state_objects = models.storage.get(State, state_id)
    if state_objects is None:
        abort(404)
    return jsonify(state_objects.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state using the state_id"""
    key = State.__name__ + '.' + state_id
    all_objects = models.storage.all()
    state = models.storage.get(State, state_id)
    if state is None:
        abort(404)
    if state and state in all_objects.values():
        del all_objects[key]
        models.storage.save()
        return jsonify('{}'), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    elif 'name' not in request.json:
        abort(400, 'Missing name')

    new_state = State(**request.json)
    models.storage.new(new_state)
    models.storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updating States"""
    if not request.is_json:
        abort(404, 'Not a JSON')
    elif 'name' not in request.json:
        abort(404, 'Missing name')
    state = models.storage.get(State, state_id)
    if state is None:
        abort(404)
    state['name'] = request.get_json().get('name')
    models.storage.save()
    return jsonify(state.to_dict()), 200
