#!/usr/bin/python3
""" Cities endpoints """
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import Flask, abort, make_response, jsonify, request


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """retrieve all city objects """
    all_cities = []
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    for cts in states.cities:
        all_cities.append(cts.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ retrieve a city based on city_id """
    citi = storage.get(City, city_id)
    if not citi:
        abort(404)
    return jsonify(citi.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ delete a city based on city_id """
    citi = storage.get(City, city_id)
    if not citi:
        abort(404)
    storage.delete(citi)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates a city object """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Misssing name")
    citi = City(**data)
    citi.state_id = states.id
    storage.new(citi)
    storage.save()
    return make_response(jsonify(citi.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ update a city based on city_id """
    citi = storage.get(City, city_id)
    if not citi:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for k, v in data.items():
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        if k not in ignore_keys:
            setattr(citi, k, v)

    citi.save()
    return make_response(jsonify(citi.to_dict()), 200)
