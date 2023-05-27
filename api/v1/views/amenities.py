#!/usr/bin/python3
"""  Amenities endpoints """
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, Flask, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves all amenities """
    amens = storage.all(Amenity).values()
    amens_list = []
    for all in amens:
        amens_list.append(all.to_dict())
    return jsonify(amens_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieve amenity based on id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Delete amenities based on amenity_id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """ Create an amenity """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Misssing name")
    amen = Amenity(**data)
    storage.new(amen)
    storage.save()
    return make_response(jsonify(amen.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ update a city based on city_id """
    amen = storage.get(Amenity, amenity_id)
    if not amen:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for k, v in data.items():
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        if k not in ignore_keys:
            setattr(amen, k, v)

    amen.save()
    return make_response(jsonify(amen.to_dict()), 200)
