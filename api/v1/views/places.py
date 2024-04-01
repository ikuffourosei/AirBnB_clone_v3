#!/usr/bin/python3
"""An API for retrieving Place data"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State
import models


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = models.storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    elif request.method == 'POST':
        body_request = request.get_json()
        if not body_request:
            abort(400, description='Not a JSON')
        if 'name' not in body_request or 'user_id' not in body_request:
            abort(400, description='Missing name or user_id')
        user_id = body_request['user_id']
        user = models.storage.get(User, user_id)
        if user is None:
            abort(404)
        new_place = Place(city_id=city_id, **body_request)
        models.storage.new(new_place)
        models.storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_modify(place_id):
    """Retrieve, delete, or update a Place object by id"""
    place = models.storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        models.storage.delete(place)
        models.storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        body_request = request.get_json()
        if not body_request:
            abort(400, description='Not a JSON')
        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, val in body_request.items():
            if key not in ignore:
                setattr(place, key, val)
        models.storage.save()
        return jsonify(place.to_dict())


@app_views.route('/places_search',methods=['GET'], srtict_slashes=False)
def search_place():
    """Search for place according to passed data"""
    search = request.get_json()
    done =  False
    if not search:
        abort(404, description='Not a JSON')
    if search == {}:
        return jsonify(models.storage.all(Place))
    elif search != {}:
        options = ['state', 'cities', 'amenities']
        for key, val in search.items():
            if key in options and key == 'state':
                state = models.storage.get(State, val)
                st_cities = [items.to_dict() for items in state.cities]
                city_ids = [items['id'] for items in st_cities]
                st_ct = [models.storage.get(City, items) for items in city_ids]
                st_ct = dict(st_ct)
                state_places = [place.to_dict() for place in st_ct.places]
                done = True
            if key in options and key == 'cities':
                city = models.storage.get(City, val)
                city_place = [place.to_dict() for place in city.places]
                done = True
            if key in options and key == 'amenities':
                #  to be implemented
                pass
        
        if done:
            if 'states' in search.keys() and 'cities' not in search.keys():
                return jsonify(state_places)
            elif 'cities' in search.keys() and 'states' not in search.keys():
                return jsonify(city_place)
            elif 'states' in search.keys() and 'cities' in search.keys():
                result = []
                result.append(state_places)
                result.append(city_place)
                return jsonify(result)
                

                    


