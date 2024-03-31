#!/usr/bin/python3
"""Blueprint of views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def index():
    '''returns a JSON: "status": "OK" '''
    return jsonify({'status': 'OK'}), 200
