from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import null, case
from app import db
from app.model import Device


class Logbook(db.Model):
    __tablename__ = "logbook"

    id = db.Column(db.Integer, primary_key=True)

    reftime = db.Column(db.DateTime, index=True)
    address = db.Column(db.String, index=True)
    takeoff_timestamp = db.Column(db.DateTime)
    takeoff_track = db.Column(db.SmallInteger)
    landing_timestamp = db.Column(db.DateTime)
    landing_track = db.Column(db.SmallInteger)
    max_altitude = db.Column(db.Float(precision=2))

    # Relations
    takeoff_airport_id = db.Column(db.Integer, db.ForeignKey("airports.id", ondelete="CASCADE"), index=True)
    takeoff_airport = db.relationship("Airport", foreign_keys=[takeoff_airport_id])

    landing_airport_id = db.Column(db.Integer, db.ForeignKey("airports.id", ondelete="CASCADE"), index=True)
    landing_airport = db.relationship("Airport", foreign_keys=[landing_airport_id])

    def get_device(self):
        return db.session.query(Device).filter(Device.address == self.address).one()

    @hybrid_property
    def duration(self):
        return None if (self.landing_timestamp is None or self.takeoff_timestamp is None) else self.landing_timestamp - self.takeoff_timestamp

    @duration.expression
    def duration(cls):
        return case({False: None, True: cls.landing_timestamp - cls.takeoff_timestamp}, cls.landing_timestamp != null() and cls.takeoff_timestamp != null())
