from .models import Image, Polygon
from .app import app
from .db import db
from .utils import get_image_polys


def parse_images(path):
    """
    loads a file pointed to by path, populating images into db
    :param path: str path to csv file containing image metadata
    :return: bool success of function
    """
    polygons = db.session.query(Polygon).all()
    # open file
    with open(path) as image_file:
        line = image_file.readline().split(',')
        while line and line[0] != '':
            if len(line) != 7:
                app.logger.error(f'input file has {len(line)} columns but we are only expecting 7')
                return False
            # extract image meta
            name, latitude, longtitude, Z, yaw, pitch, roll = line
            # read next line
            line = image_file.readline().split(',')
            # make sure there is no prior image by this name
            if db.session.query(Image.name).filter(Image.name==name).first():
                app.logger.debug(f'Image {name} already in db')
                continue
            # create image instances
            im = Image.create(name, latitude, longtitude, Z, yaw, pitch, roll)
            if not im:
                app.logger.debug(f'failed to create {im}')
            else:
                app.logger.debug(f'added {im}')
                db.session.add(im)
                polys = get_image_polys(im, polygons)
                app.logger.debug(f'got polys {polys}')
                for p in polys:
                    p.images.append(im)
                    db.session.add(p)
    try:
        db.session.commit()
        return True
    except Exception as e:
        app.logger.error(f'Failed to commit session with error:\n{e}')
        db.session.rollback()
    return False
