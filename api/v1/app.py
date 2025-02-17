#!/usr/bin/python3
""" Flask application """
from api.v1.views import app_views
from flask_cors import CORS
from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from os import getenv

app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(exception):
    """ Closes a session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
