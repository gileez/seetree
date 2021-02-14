import json
from .models import Image, Polygon, Point
from .app import app
from .db import db
from .utils import get_images_for_poly


def parse_polygons(path):
    """
    insers polygons into db from a geojson pointed to by path
    :param path: str path to geojson file
    :return:
    """

    # load geo object
    with open(path) as geo_file:
        geo = json.load(geo_file)
    # get all images
    images = db.session.query(Image).all()
    for poly in geo['features']:
        if poly.get('geometry', {}).get('type') != 'Polygon':
            # this is not a polygon
            continue
        index = poly['properties']['index']
        # make sure there is no such polygon
        if db.session.query(Polygon.index).filter(Polygon.index==index).first():
            # we already have a polygon by this name
            app.logger.error(f'Polygon {index} already exists')
            continue
        created_on = poly['properties']['createdAt']
        farm_id = poly['properties']['farmID']
        id = poly['properties']['id']
        zone_id = poly['properties']['zoneID']
        point_instances = []
        points = []
        # generate all points
        for point in poly['geometry']['coordinates'][0]:
            p = Point.create(point[1], point[0])
            point_instances.append(p)
            points.append((point[1], point[0]))
        # get all images matching this polygon
        poly_images = get_images_for_poly(images, points)
        poly_instance = Polygon.create(index=index, images=poly_images, points=point_instances, zone_id=zone_id,
                                       id=id, farm_id=farm_id, created_on=created_on)
        db.session.add(poly_instance)
        app.logger.debug(f'Added {poly_instance} to session')
    try:
        db.session.commit()
        return True
    except Exception as e:
        app.logger.error(f'Failed to commit session with error:\n{e}')
        db.session.rollback()
    return False
