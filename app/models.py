import os
import uuid
from datetime import datetime
from app import db
from pyechonest import config
from pyechonest import artist as en_artist
from pyechonest import song as en_song

config.ECHO_NEST_API_KEY = os.getenv("ECHO_NEST_API_KEY")

groups_songs = db.Table(
    "groups_songs",
    db.Column("song_id", db.Integer, db.ForeignKey("song.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("group.id")),
)

users_songs = db.Table(
    "users_songs",
    db.Column("song_id", db.Integer, db.ForeignKey("song.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    songs = db.relationship("Song", secondary=users_songs, backref="users", lazy="dynamic")
    groups = db.relationship("Group", backref="user", lazy="dynamic")
    performances = db.relationship("Performance", backref="user", lazy="dynamic")
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    email = db.Column(db.String(256), unique=True)
    image_url = db.Column(db.String(256), unique=True)
    uuid = db.Column(db.String(36))
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(
        self,
        email=None,
        first_name=None,
        last_name=None,
        latitude=None,
        longitude=None,
        image_url=None,

    ):
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        self.email = email
        self.image_url = image_url
        self.uuid = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return "<User %s %s %s>" % (self.first_name, self.last_name, self.email)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    songs = db.relationship("Song", secondary=groups_songs, backref="groups", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    #TODO: order of songs within set
    name = db.Column(db.String(256))
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __init__(
        self,
        user,
        name=None,
    ):
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        self.user = user
        self.name = name

    def __str__(self):
        return "<Group %s>" % (self.name)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    echonest_id = db.Column(db.String(18))
    songsterr_id = db.Column(db.String(18))
    rdio_id = db.Column(db.String(18))
    songs = db.relationship("Song", backref="artist", lazy="dynamic")

    def __init__(
        self,
        name,
        songsterr_id=None,
        rdio_id=None,
    ):
        self.name = name
        self.echonest_id = en_artist.Artist(name).id
        self.songsterr_id = songsterr_id
        self.rdio_id = rdio_id

    def __str__(self):
        return "<Artist %s %s>" % (self.name)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))
    name = db.Column(db.String(256))
    file_url = db.Column(db.String(256))
    echonest_id = db.Column(db.String(18))
    songsterr_id = db.Column(db.String(18))
    rdio_id = db.Column(db.String(18))
    key = db.Column(db.String(10))
    tempo = db.Column(db.Float)
    loudness = db.Column(db.Float)
    major_key = db.Column(db.Boolean)

    def __init__(
        self,
        name,
        artist,
        file_url=None,
        echonest_id=None,
        songsterr_id=None,
        rdio_id=None,
        key=None,
        tempo=None,
        loudness=None,
        major_key=None,
        genre=None,
    ):
        en_result = en_song.search(artist=artist.name, title=name, results=1)[0]
        en_summary = en_result.get_audio_summary()
        print en_result.title
        print en_summary
        self.name = name
        self.artist = artist
        self.file_url = file_url
        self.echonest_id = en_result.id
        self.songsterr_id = songsterr_id
        self.rdio_id = rdio_id
        self.key = en_summary[u"key"]
        self.tempo = en_summary[u"tempo"]
        self.loudness = en_summary[u"loudness"]
        self.major_key = en_summary[u"mode"]
        self.genre = genre

    def __str__(self):
        return "<Song %s - %s>" % (self.artist.name, self.name)


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    performances = db.relationship("Performance", backref="venue", lazy="dynamic")
    name = db.Column(db.String(80))
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    fb_id = db.Column(db.String(16))

    def __init__(
        self,
        name,
        latitude=None,
        longitude=None,
        fb_id=None
    ):
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.fb_id = fb_id

    def __str__(self):
        return "<Venue %s>" % (self.name)


class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"))
    name = db.Column(db.String(80))
    start = db.Column(db.DateTime)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __init__(
        self,
        name,
        start,
    ):
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        self.name = name
        self.start = start

    def __str__(self):
        return "<Performance %s %s %s %s>" % (
            self.name,
            self.user.first_name,
            self.user.last_name,
            self.start.isoformat()
        )
