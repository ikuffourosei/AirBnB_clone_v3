#!/usr/bin/python3
"""Blueprint of views"""
from api.v1.views import app_views
from flask import jsonify
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State


classes = {'Amenity': Amenity,
           'BaseModel': BaseModel,
           'City': City,
           'Place': Place,
           'Review': Review,
           'User': User,
           'State': State
           }


@app_views.route('/status', methods=['GET'])
def index():
    '''returns a JSON: "status": "OK" '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def index_stats():
    """an endpoint that retrieves the number of each objects by type:"""
    data = {}
    for key, val in classes.items():
        data[key] = models.storage.count(val)
    #  sorting the data
    lista = list(data.keys())
    lista.sort()
    sorted_dict = {k: data[k] for k in lista}
    return jsonify(sorted_dict)
