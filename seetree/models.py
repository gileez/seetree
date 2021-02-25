from seetree.db import db
from datetime import datetime

class Image(db.Model):
    __tablename__ = 'images'
    name = db.Column(db.String(128), primary_key=True)
    latitude = db.Column(db.Float(), nullable=False)
    longtitude = db.Column(db.Float(), nullable=False)
    Z = db.Column(db.Float(), nullable=False)
    yaw = db.Column(db.Float(), nullable=False)
    pitch = db.Column(db.Float(), nullable=False)
    roll = db.Column(db.Float(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return "<Image:{}>".format(self.name)
    @staticmethod
    def create(name, latitude, longtitude, Z, yaw, pitch, roll):
        # populates a new image in the db
        im = Image(name=name, latitude=float(latitude), longtitude=float(longtitude), Z=float(Z), yaw=float(yaw),
                   pitch=float(pitch), roll=float(roll))
        return im

    def to_json(self):
        return {k: getattr(self, k) for k in self.__dict__ if k[0] != '_'}


polygon_images = db.Table('polygon_images',
    db.Column('polygon_index', db.String(128), db.ForeignKey('polygons.index')),
    db.Column('image_name', db.String(128), db.ForeignKey('images.name'))
)


class Polygon(db.Model):
    __tablename__ = 'polygons'
    index = db.Column(db.String(128), primary_key=True)
    id = db.Column(db.String(20), index=True)
    points = db.relationship('Point')
    images = db.relationship('Image', secondary=polygon_images, backref='polygons')
    zone_id = db.Column(db.String(128), nullable=False)
    farm_id = db.Column(db.String(128), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return "<Polygon:{}>".format(self.index)

    @staticmethod
    def create(index, id, images, points, zone_id, farm_id, created_on):
        # generate a new polygon
        poly = Polygon(index=index, id=id, images=images, points=points, zone_id=zone_id, farm_id=farm_id,
                       created_on=datetime.fromtimestamp(created_on/1000.0))
        return poly

    def get_points(self):
        return [p.to_list() for p in self.points]

    def get_points_json(self):
        return {"geometry": {"coordinates": [self.get_points()]}}

    def to_json(self):
        return {"index": self.index, "points": self.get_points_json(), "zone_id": self.zone_id, "farm_id": self.farm_id,
                "created_on": self.created_on}



class Point(db.Model):
    __tablename__ = 'points'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    latitude = db.Column(db.Float(), nullable=False)
    longtitude = db.Column(db.Float(), nullable=False)
    poly_index = db.Column(db.String(128), db.ForeignKey('polygons.index'))

    def __repr__(self):
        return "<Point:{},{}>".format(self.latitude, self.longtitude)

    @staticmethod
    def create(latitude, longtitude):
        # generates a new point
        p = Point(latitude=float(latitude), longtitude=float(longtitude))
        return p

    def to_list(self):
        return [self.latitude, self.longtitude]