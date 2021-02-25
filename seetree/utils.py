from shapely.geometry import Point, Polygon


def get_images_for_poly(images, points):
    """
    converts points into a poly and checks which image is in the poly
    :param images: list of tuples(index,lat,lon)
    :param points: list of tuples(lat,lon)
    :return: list of image indexes
    """
    poly = Polygon(points)
    res = []
    for im in images:
        p = Point(im.latitude, im.longtitude)
        if p.within(poly):
            res.append(im)
    return res


def get_image_polys(image, polygons):
    """
    cycles all polygons in search for an intersecting image
    :param image: db object
    :param polygons: list of all db polygons
    :return: list of polygons to be linked to this image
    """
    res = []
    im_point = Point((image.latitude, image.longtitude))
    for p in polygons:
        poly = Polygon(map(tuple, p.get_points()))
        if im_point.within(poly):
            res.append(p)
    return res
