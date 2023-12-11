from datetime import datetime

from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    type = db.Column(db.String(150))


class ServiceProvider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    type = db.Column(db.String(255), nullable=False)
    contacts = db.Column(db.String(255))
    details = db.Column(db.String(255))

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    street = db.Column(db.String(255), nullable=True)
    details = db.Column(db.String(255), nullable=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    time = db.Column(db.Time, nullable=True)
    event_type = db.Column(db.String(255))

    status = db.Column(db.String(255))

    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location', backref='locations', lazy=True,
                                 foreign_keys=[location_id])

    photo_video_id = db.Column(db.Integer, db.ForeignKey('service_provider.id'))
    photo_video = db.relationship('ServiceProvider', backref='events_photo_video', lazy=True,
                                  foreign_keys=[photo_video_id])

    music_id = db.Column(db.Integer, db.ForeignKey('service_provider.id'))
    music = db.relationship('ServiceProvider', backref='events_music', lazy=True,
                            foreign_keys=[music_id])

    moderators_id = db.Column(db.Integer, db.ForeignKey('service_provider.id'))
    moderators = db.relationship('ServiceProvider', backref='events_moderators', lazy=True,
                                 foreign_keys=[moderators_id])

    dancers = db.Column(db.String(255))
    mires = db.Column(db.String(255))
    contacts = db.Column(db.String(255))
    details = db.Column(db.Text)
    culoarea = db.Column(db.Text)
    price = db.Column(db.Text)
    avans = db.Column(db.Text)

