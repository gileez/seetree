from flask import Blueprint, request, jsonify
import os
from seetree.db import db
from seetree.parsers import parse_polygons, parse_images
from seetree.models import Image, Polygon

api_bp = Blueprint('api', __name__, url_prefix='/api')
session = db.session


@api_bp.route('/load_images', methods=['POST'])
def load_images():
    # extract file path
    path = request.get_json().get('path')
    # make sure file exists
    if not os.path.isfile(path):
        return f'File does not exist: {path}', 404
    # pass on to handler
    if parse_images.delay(path):
        return '', 201
    else:
        return f'Failed to load images from {path}', 500


@api_bp.route('/load_polygons', methods=['POST'])
def load_polygons():
    # extract file path
    path = request.get_json().get('path')
    # make sure file exists
    if not os.path.isfile(path):
        return f'File does not exist: {path}', 404
    # pass on to handler
    parse_polygons.delay(path)
    return f'Request to process {path} passed to Celery', 201


@api_bp.route('/get_polygon', methods=['POST'])
def get_polygon():
    # get instance from database using polygon index
    index = request.get_json().get('index')
    res = session.query(Polygon).filter(Polygon.index==index).first()
    if res:
        return jsonify(res.to_json()), 200
    return f'Polygon {index} not found', 404


@api_bp.route('/get_image', methods=['POST'])
def get_image():
    # get instance from database using image name
    name = request.get_json().get('name')
    res = session.query(Image).filter(Image.name==name).first()
    if res:
        return jsonify(res.to_json()), 200
    return f'Image {name} not found', 404


@api_bp.route('/all_polygons', methods=['GET'])
def get_polygons():
    # query all polygons with a relationship to an image
    res = session.query(Polygon).filter(Polygon.images.any()).all()
    if res:
        return jsonify([p.index for p in res]), 200
    return f'No polygons found pointing to images', 200


