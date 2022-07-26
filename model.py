from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Venue(db.Model):
    __tablename__='venue'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, unique=True)
    city=db.Column(db.String(120))
    state=db.Column(db.String(120))
    address=db.Column(db.String(120), unique=True)
    phone=db.Column(db.String(120), unique=True)
    image_link=db.Column(db.String(500))
    facebook_link=db.Column(db.String(120))
    genres=db.Column(db.String(500))
    website_link=db.Column(db.String(120))
    is_seeking=db.Column(db.Boolean())
    seeking_description=db.Column(db.String(1040))
    has_image=db.Column(db.Boolean())
    shows=db.relationship('Show', backref='venue_show', lazy=True)
    venue_genres=db.relationship('VenueGenre', backref="venue_genre", 
        lazy=True)

class Artist(db.Model):
    __tablename__='artist'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, unique=True)
    city=db.Column(db.String(120))
    state=db.Column(db.String(120))
    phone=db.Column(db.String(120), unique=True)
    genres=db.Column(db.String(500))
    image_link=db.Column(db.String(500))
    facebook_link=db.Column(db.String(120))
    is_seeking=db.Column(db.Boolean())
    website_link=db.Column(db.String(120))
    seeking_description=db.Column(db.String(1040))
    has_image=db.Column(db.Boolean())
    shows=db.relationship('Show', backref='artist_show', lazy=True)
    artist_genres=db.relationship('ArtistGenre', backref="artist_genre", 
        lazy=True)

class Show(db.Model):
    __tablename__="show"

    id=db.Column(db.Integer, primary_key=True)
    venue_id=db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id=db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    start_time=db.Column(db.DateTime, nullable=False)
    end_time=db.Column(db.DateTime, nullable=False)
    all_day=db.Column(db.Boolean, default=False)

class Genre(db.Model):
    __tablename__="genre"

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, unique=True)

class ArtistGenre(db.Model):
    __tablename__="artist_genre"

    id=db.Column(db.Integer, primary_key=True)
    artist_id=db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    genre_id=db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)

class ArtistAvail(db.Model):
    __tablename__="artist_avail"

    id=db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
    sun = db.Column(db.Boolean, default=True)
    mon = db.Column(db.Boolean, default=True)
    tue = db.Column(db.Boolean, default=True)
    wed = db.Column(db.Boolean, default=True)
    thu = db.Column(db.Boolean, default=True)
    fri = db.Column(db.Boolean, default=True)
    sat = db.Column(db.Boolean, default=True)

class VenueGenre(db.Model):
    __tablename__="venue_genre"

    id=db.Column(db.Integer, primary_key=True)
    venue_id=db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    genre_id=db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
