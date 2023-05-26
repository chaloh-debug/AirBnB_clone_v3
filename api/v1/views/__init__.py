#!/usr/bin/python3
""" Init """
from flask import Blueprint
from models import storage
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
