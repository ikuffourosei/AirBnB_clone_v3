#!/usr/bin/python3
"""
route for handling Amenity objects and operations
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def view_amenities():
    """Returns a list containing all Amenity objects"""
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new amenity object"""
    amenity_data = request.get_json(silent=True)
    if not amenity_data:
        raise abort(400, description="Not a JSON")
    if 'name' not in request.json:
        raise abort(400, description="Missing name")
    new_amenity = Amenity(**amenity_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def view_amenity(amenity_id):
    """Returns the amenity with id 'amenity_id'"""
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['PUT', 'PATCH'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates the amenity with id 'amenity_id'"""
    amenity_dict = request.get_json(silent=True)
    if not amenity_dict:
        raise abort(400, description="Not a JSON")
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            for k, v in amenity_dict.items():
                if k != 'id' and k != 'created_at' and k != 'updated_at':
                    setattr(amenity, k, v)
            amenity.save()
            return jsonify(amenity.to_dict()), 200
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes the amenity with id 'amenity_id'"""
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
    abort(404)
