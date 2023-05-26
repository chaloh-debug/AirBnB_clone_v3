#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint
from models import storage

@app_views.route('/status', strict_slashes=False)
def status():
    """ Status of API """
    stat = {"status": "OK"}
    return jsonify(stat)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    models = {"User": "users", "Amenity": "amenities", "Place": "places",
              "Review": "reviews", "City": "cities", "State": "states"}
    stats = {}
    for k in models.keys():
        stats[models[k]] = storage.count(k)
    return jsonify(stats)
