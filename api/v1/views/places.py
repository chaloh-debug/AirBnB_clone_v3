#!/usr/bin/python3
""" places endpoints """
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views
from flask import Flask, abort, make_response, jsonify, request


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """retrieve all place objects """
    city_places = []
    city = storage.get('City', city_id)
    places = storage.all(Place)
    if not city or not places:
        abort(404)
    for place in places.values():
        if place.city_id == city_id:
            city_places.append(place.to_dict())
    return jsonify(city_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ retrieve a place based on id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ delete a place based on id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates a place object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Misssing name")
    users = storage.all(User)
    found = False
    for user in users.values():
        if user.id == data.user_id:
            found = True
    if not found:
        abort(404)
    place = Place(**data)
    place.city_id = city.id
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ update a place based on id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for k, v in data.items():
        ignore_keys = ['id', 'user_id', 'created_at', 'updated_at']
        if k not in ignore_keys:
            setattr(place, k, v)

    place.save()
    return make_response(jsonify(place.to_dict()), 200)
