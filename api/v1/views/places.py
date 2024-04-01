#!/usr/bin/python3
"""An API for retrieving Place data"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
from models.amenity import Amenity
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_place():
    """Search for place according to passed data"""
    search = request.get_json()
    if not search:
        abort(400, description='Not a JSON')
    if search == {}:
        all_places = models.storage.all(Place).values()
        places = [place.to_dict() for place in all_places]
        return jsonify(places)
    state_places = []
    pl_city = []
    amenities_places = []
    options = ['states', 'cities', 'amenities']
    for key, val in search.items():
        if key == 'states':
            for state_id in val:
                state = models.storage.get(State, state_id)
                if state:
                    state_places.extend([place.to_dict()
                                         for city in state.cities
                                         for place in city.places])
        elif key == 'cities':
            for city_id in val:
                city = models.storage.get(City, city_id)
                if city:
                    pl_city.extend([place.to_dict() for place in city.places])
        elif key == 'amenities':
            for amenity_id in val:
                amenity = models.storage.get(Amenity, amenity_id)
                if amenity:
                    amenities_places.extend([place.to_dict() for place in
                                             models.storage.all(Place).values()
                                             if amenity in place.amenities])
    result = []
    if 'states' in search and 'cities' in search:
        result = [place for place in state_places if place in pl_city]
    elif 'states' in search:
        result = state_places
    elif 'cities' in search:
        result = pl_city
    if 'amenities' in search:
        result = [place for place in result if place in amenities_places]

    return jsonify(result)
