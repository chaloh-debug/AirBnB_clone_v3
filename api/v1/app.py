#!/usr/bin/python3
""" Flask application """
from api.v1.views import app_views
from flask import Flask, Blueprint
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_app(exception):
    """ Closes a session """
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
