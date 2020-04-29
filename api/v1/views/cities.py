#!/usr/bin/python3
"""
File to work with Amenities
"""

from models.base_model import *
from api.v1.views import app_views
from models import storage
from models.city import *
from models.state import State
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def cities_by_state(state_id):
    """Function that retrieve and save a new City"""
    state = storage.get(State, state_id)
    cities = storage.all('City').values()
    ls = []
    if state:
        for city in cities:
            if city.state_id == state_id:
                ls.append(city.to_dict())
        if request.method == "GET":
            return jsonify(ls)
        elif request.method == "POST":
            if not request.json:
                return make_response(jsonify(
                                     {'error': "Not a JSON"}), 400)
            elif 'name' not in request.json:
                return make_response(jsonify(
                                     {'error': "Missing name"}), 400)
            else:
                json = request.json
                json['state_id'] = state_id
                new = City(**json)
                new.save()
                return make_response(new.to_dict(), 201)
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def city(city_id):
    """Function that retrieve, delete and put a City"""
    city = storage.get(City, city_id)
    if city:
        if request.method == "GET":
            return city.to_dict()
        elif request.method == "DELETE":
            storage.delete(city)
            storage.save()
            return {}
        elif request.method == "PUT":
            if not request.json:
                return make_response(jsonify({'error': "Not a JSON"}), 400)
            else:
                json = request.json
                for key, value in json.items():
                    if key != 'id' and key != 'state_id' and\
                       key != 'created_at' and key != "updated_at":
                        setattr(city, key, value)
                city.updated_at = datetime.utcnow()
                storage.save()
                return make_response(city.to_dict(), 200)
    abort(404)
