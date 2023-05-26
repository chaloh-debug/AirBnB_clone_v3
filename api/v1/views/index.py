#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint


@app_views.route('/status', strict_slashes=False)
def status():
    """ Status of API """
    stat = {"status": "OK"}
    return jsonify(stat)
