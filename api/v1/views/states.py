#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """retrieve all state objects """
    all_states = []
    for state in storage.all(State).values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id=None):
    """retrieves a state object by id"""
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """deletes a state object"""
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a state object"""
    try:
        json_data = request.get_json()
    except exception as e:
        json_data = None
    if json_data is None:
        return 'Not a JSON', 400
    if "name" not in json_data.keys():
        return 'Missing name', 400
    state = State(**json_data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """update a state object"""
    try:
        if state_id is None:
            abort(404)
        json_data = request.get_json()
    except exception as e:
        json_data = None
    if json_data is None:
        return 'Not a JSON', 400
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    json_data.pop('id', None)
    json_data.pop('created_at', None)
    json_data.pop('updated_at', None)
    for k, v in json_data.items():
        setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
