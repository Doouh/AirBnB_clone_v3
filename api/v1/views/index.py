#!/usr/bin/python3
"""
File to work with Amenities
"""

from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Function that return status"""
    return ({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Function that return the count of objects"""
    classes = {"users": 'User', "states": 'State', "amenities": 'Amenity',
               "cities": 'City', "places": 'Place', "reviews": 'Review'}
    json = {}
    for key, value in classes.items():
        json[key] = storage.count(value)
    return json
