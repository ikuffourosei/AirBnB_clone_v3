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
    state = models.storage.get(State, state_id)
    if state is None:
        abort(404)
    models.storage.delete(state)
    models.storage.save()
    return jsonify('{}'), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State"""
    body_request = request.get_json()
    if not body_request:
        abort(404, description='Not a JSON')
    if 'name' not in request.json:
        abort(404, description='Missing name')
    new_state = State(**body_request)
    models.storage.new(new_state)
    models.storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updating States"""
    body_response = request.get_json()
    if not body_response:
        abort(400, description='Not a JSON')
    if 'name' not in body_response:
        abort(400, description='Missing name')
    state = models.storage.get(State, state_id)
    if not state:
        abort(404)
    for k, v in body_response.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
