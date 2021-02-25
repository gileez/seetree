import json
from seetree.models import Image, Polygon, Point
from seetree.db import get_engine_session
from seetree.utils import get_images_for_poly, get_image_polys
from seetree.celery_app import celery_app
import logging

@celery_app.task
def parse_polygons(path):
    """
    inserts polygons into db from a geojson pointed to by path
    :param path: str path to geojson file
    :return: boolean success of function
    """
    # load geo object
    with open(path) as geo_file:
        geo = json.load(geo_file)
    # generate db session
    _, session = get_engine_session()
    # get all images
    images = session.query(Image).all()
    for poly in geo['features']:
        if poly.get('geometry', {}).get('type') != 'Polygon':
            # this is not a polygon
            continue
        index = poly['properties']['index']
        # make sure there is no such polygon
        if session.query(Polygon.index).filter(Polygon.index==index).first():
            # we already have a polygon by this name
            logging.debug(f'Polygon {index} already exists')
            continue
        # extract poly meta
        # todo protect extraction
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
        session.add(poly_instance)
        logging.debug(f'Added {poly_instance} to session')
    try:
        session.commit()
        return True
    except Exception as e:
        logging.error(f'Failed to commit session with error:\n{e}')
        session.rollback()
        raise


@celery_app.task
def parse_images(path):
    """
    loads a file pointed to by path, populating images into db
    :param path: str path to csv file containing image metadata
    :return: bool success of function
    """
    # generate db session
    _, session = get_engine_session()
    polygons = session.query(Polygon).all()
    # open file
    with open(path) as image_file:
        line = image_file.readline().split(',')
        while line and line[0] != '':
            if len(line) != 7:
                logging.error(f'input file has {len(line)} columns but we are only expecting 7')
                raise
            # extract image meta
            name, latitude, longtitude, Z, yaw, pitch, roll = line
            # read next line
            line = image_file.readline().split(',')
            # make sure there is no prior image by this name
            if session.query(Image.name).filter(Image.name==name).first():
                logging.debug(f'Image {name} already in db')
                continue
            # create image instances
            im = Image.create(name, latitude, longtitude, Z, yaw, pitch, roll)
            if not im:
                logging.error(f'Failed to create {im}')
            else:
                session.add(im)
                logging.debug(f'added {im}')
                polys = get_image_polys(im, polygons)
                logging.debug(f'got polys {polys}')
                for p in polys:
                    p.images.append(im)
                    session.add(p)
    try:
        session.commit()
        return True
    except Exception as e:
        logging.error(f'Failed to commit session with error:\n{e}')
        session.rollback()
        raise

