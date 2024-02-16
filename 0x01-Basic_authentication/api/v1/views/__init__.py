#!/usr/bin/env python3
"""Defines API views."""
from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.users import *
from models.user import User

# Production-ready: Creating a Blueprint for API version 1
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

User.load_from_file()
