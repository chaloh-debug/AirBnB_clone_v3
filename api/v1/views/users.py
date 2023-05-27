#!/usr/bin/python3
"""  Users endpoints """
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import abort, Flask, jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves all users """
    users = storage.all(User).values()
    users_list = []
    for all in users:
        users_list.append(all.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Retrieve user based on id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Delete user based on user_id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """ Create an user """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Misssing name")
    user = User(**data)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """ update a user based on user_id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for k, v in data.items():
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        if k not in ignore_keys:
            setattr(user, k, v)

    user.save()
    return make_response(jsonify(user.to_dict()), 200)
