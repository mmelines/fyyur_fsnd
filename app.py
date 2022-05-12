#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
db.app = app
db.init_app(app)
migrate = Migrate(app, db)
db.create_all()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(120), unique=True)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genre_list = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    is_seeking = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(1040))
    has_image = db.Column(db.Boolean())
    shows = db.relationship('Show', backref='venue_show', lazy=True)
    genres = db.relationship('VenueGenre', backref="venue_genre", lazy=True)

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120), unique=True)
    genre_list = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    is_seeking = db.Column(db.Boolean())
    website_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(1040))
    has_image = db.Column(db.Boolean())
    shows = db.relationship('Show', backref='artist_show', lazy=True)
    genres = db.relationship('ArtistGenre', backref="artist_show", lazy=True)

class Show(db.Model):
    __tablename__ = "show"

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    all_day = db.Column(db.Boolean)

class ArtistGenre(db.Model):
    __tablename__ = "artist_genres"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))

class VenueGenre(db.Model):
    __tablename__ = "venue_genres"

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))

class Genre(db.Model):
    __tablename__ = "genre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    # relationships
    artists = db.relationship('ArtistGenre', backref='genre_artist', lazy=True)
    genres = db.relationship('VenueGenre', backref='genre_venue', lazy=True)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, datetime):
    value = str(value)
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime
#----------------------------------------------------------------------------#
# Custom Classes
#----------------------------------------------------------------------------#

class Obj:

  def __init__(self):
    """
    init attributes common to Artist and Venue class objects
    """
    self.entity_type = None
    self.id = False
    self.name = False
    self.state = False
    self.city = False
    self.phone = False
    self.image_link = False
    self.facebook_link = False
    self.website_link = False
    self.is_seeking = False
    self.seeking_description = False
    self.has_image = False
    self.genre_list = False
    self.shows = None #TODO
    self.past_shows = None #TODO
    self.upcoming_shows = None #TODO
    self.genres = None #TODO

  def form(self, request):
    """
    populate entity with data from a POST request
    """
    self.name = request.form.get('name')
    self.state = request.form.get('state')
    self.city = request.form.get('city')
    if self.entity_type == "venue":
      self.address = request.form.get('address')
    self.phone = request.form.get('phone')
    self.image_link = request.form.get('image_link')
    self.facebook_link = request.form.get('facebook_link')
    self.genre_list = request.form.get('genre_list')
    self.is_seeking = request.form.get('is_seeking')
    self.website_link = request.form.get('website_link')
    self.seeking_description = request.form.get('seeking_description')
    self.has_image = request.form.get('has_image')

  def copy(self, obj):
    """
    populate entity with data from a SQLAlchemy object
    """
    self.id = obj.id
    self.name = obj.name
    self.state = obj.state
    self.city = obj.city
    if self.entity_type == "venue":
      self.address = obj.address
    self.phone = obj.phone
    self.image_link = obj.image_link
    self.facebook_link = obj.facebook_link
    self.genre_list = obj.genre_list
    self.is_seeking = obj.is_seeking
    self.website_link = obj.website_link
    self.seeking_description = obj.seeking_description
    self.has_image = obj.has_image
    self.list_genres()
    #self.shows = self.show(obj.shows)

  def list_genres(self):
    if isinstance(self.genre_list, str):
      genres = self.genre_list[1:-1].split(',')
      self.genre_list = genres

  def __iter__(self):
    """
    iterator properties of generic object
    """
    yield ("name", self.name)
    yield ("state", self.state)
    yield ("city", self.city)
    yield ("phone", self.phone)
    yield ("image_link", self.image_link)
    yield ("facebook_link", self.facebook_link)
    yield ("genre_list", self.genre_list)
    yield ("is_seeking", self.is_seeking)
    yield ("seeking_description", self.seeking_description)
    yield ("has_image", self.has_image)
    yield ("shows", self.shows)

  def __repr__(self):
    """
    string representation of entity instance
    """
    msg = "id: " + str(self.id) + "; "
    msg += "name: " + str(self.name) + "\n"
    msg += "state: " + str(self.state) + "\n"
    msg += "city: " + str(self.city) + "\n"
    msg += "phone: " + str(self.phone) + "\n"
    msg += "image_link: " + str(self.image_link) + "\n"
    msg += "facebook_link: " + str(self.facebook_link) + "\n"
    msg += "genre_list: " + str(self.genre_list) + "\n"
    msg += "is_seeking: " + str(self.is_seeking) + "\n"
    msg += "seeking_description: " + str(self.seeking_description) + "\n"
    msg += "has_image: " + str(self.has_image) + "\n"
    msg += "shows: " + str(self.shows) + "\n"
    return msg

  @staticmethod
  def flash(obj):
    """
    generate messages to be flashed in common situations
    """
    data = {"failure": True,
            "msg": "Could not create venue obj. "}
    pprint(obj)
    if not obj is None:
      if "name" in obj.keys():
        if obj["error"] == False:
          msg = 'Venue ' + obj["name"] + " was listed successfully"
          data = obj
        else:
          #
          if obj["error_info"].find("UniqueViolation"):
            error_msg = obj["error_info"][obj["error_info"].find("DETAIL"):]
            error_msg = error_msg.split("=")
            field = error_msg[0][error_msg[1].find("("):-1]
            value = error_msg[1][1:error_msg[1].find(")") + 1]
            msg = "Venue " + obj["name"] + " couldn't be created because its "
            msg += field + value + " already exists in the database."
          #
          else: 
            msg = "Oops! Something went wrong on our end. "
            if obj["name"] != False:
              msg += 'Venue ' + obj["name"] + " could not be listed. "
            msg += "Please try again later."
          data["msg"] = msg
        flash(msg)
      else:
        data["msg"] += "Invalid Form submission."
    else:
      data["msg"] += "Form not recieved."
    return datas

  @staticmethod
  def add_error_msg(sys_error):
    """
    format error message from system error and return it as a string
    """
    print("ADD ERROR MSG: " + str(type(sys_error)))
    print(sys_error)
    string = ""
    for item in sys_error:
      string += str(item)
    return string

  def get_shows(self):
    if self.entity_type == "artist":
      shows = Show.query.filter_by(artist_id=self.id).all()
    if self.entity_type == "venue":
      shows = Show.query.filter_by(venue_id=self.id).all()
    return shows

  def set_shows(self):
    def append_pair(show, entity_type):
      if entity_type == "artist":
        if not show.venue_id in pairs.keys():
          venue = Venue.query.filter_by(id=show.venue_id).one()
          show.venue_image_link = venue.image_link
          show.venue_name = venue.name
          pairs[show.venue_id] = {"name": venue.name,
                                  "img": venue.image_link}
        else:
          show.venue_image_link = pairs[show.venue_id]["img"]
          show.venue_name = pairs[show.venue_id]["name"]
      if entity_type == "venue":
        if not show.venue_id in pairs.keys():
          artist = Artist.query.filter_by(id=show.artist_id).one()
          show.artist_image_link = artist.image_link
          show.artist_name = artist.name
          pairs[show.artist_id] = {"name": artist.name,
                                  "img": artist.image_link}
        else:
          show.artist_image_link = pairs[show.artist_id]["img"]
          show.artist_name = pairs[show.artist_id]["name"]
      return show

    shows = self.get_shows()
    pairs = {}
    for show in shows:
      new_show = append_pair(ShowObj().copy(show), self.entity_type)
      if self.shows is None:
        self.shows = {new_show.show_id : new_show}
      else:
        if not new_show.show_id in self.shows.keys():
          self.shows[new_show.show_id] = new_show
      now = datetime.now()
      if new_show.start_time < now:
        if not isinstance(self.past_shows, list):
          self.past_shows = []
        self.past_shows.append(new_show)
      else:
        if not isinstance(self.upcoming_shows, list):
          self.upcoming_shows = []
        self.upcoming_shows.append(new_show)
    return self

class ArtistObj(Obj):
  """
  Handles common functions of Artist objects
  """

  def __init__(self, **kwargs):
    super().__init__()
    self.entity_type = "artist"

  def get_artist(self, artist_id):
    """
    return sqlalchemy model of one artist entity
    takes one input parameter:
     - artist_id: primary key of artist
    returns status (boolean). True if success and False if failure
    """
    artist = Artist.query.get(artist_id)
    self.copy(artist)
    self.list_genres()
    return self

  def form_artist(self, form):
    """
    generate new artist from form data and commit to db
    if error, direct to handle_error() before returning
    takes one input paramerter:
     - form:
    returns status (boolean). True if success and False if failure
    """
    return "TODO"

  def edit_artist(self, original, form):
    """
    generate artist edit based on form input
    if error, direct to handle_error() before returning
    takes two input parameters:
    - artist: original artist object with given data
    - form: response of POST request
    returns status (boolean). True if success and False if failure
    """
    return "TODO"

class VenueObj(Obj):
  """
  Handles common functions of Venue objects
  """

  def __init__(self, **kwargs):
    super().__init__()
    self.entity_type = "venue"

  def get_venue(self, venue_id):
    """
    return sqlalchemy model of one venue entity
    takes one input parameter:
     - venue_id: primary key of venue
    returns self
    """
    venue = Venue.query.get(venue_id)
    self.copy(venue)
    self.list_genres()
    return self

  def form_venue(self, form):
    """
    generate new venue from form data and commit to db
    if error, direct to handle_error() before returning
    takes one input paramerter:
     - form:
    returns status (boolean). True if success and False if failure
    """
    return "TODO"

  def edit_venue(self, original, form):
    """
    generate venue edit based on form input
    if error, direct to handle_error() before returning
    takes two input parameters:
    - venue: original venue object with given data
    - form: response of POST request
    returns status (boolean). True if success and False if failure
    """
    return "TODO"

class ShowObj:

  def __init__(self):
    """
    init instance of class ShowObj
    """
    self.show_id = None
    self.venue_id = None
    self.artist_id = None
    self.start_time = None
    self.end_time = None
    self.all_day = None
    self.artist_image_link = None
    self.venue_image_link = None

  def form(self, request):
    """
    """
    self.show_id = request.form.get('show_id')
    self.venue_id = request.form.get('venue_id')
    self.artist_id = request.form.get('artist_id')
    self.start_time = request.form.get('start_time')
    self.end_time = request.form.get('end_time')
    self.all_day = request.form.get('all_day')
    return self

  def copy(self, obj):
    """
    """
    self.show_id = obj.id
    self.venue_id = obj.venue_id
    self.artist_id = obj.artist_id
    self.start_time = obj.start_time
    self.end_time = obj.end_time
    self.all_day = obj.all_day
    return self

  def __iter__(self):
    """
    """
    yield ("show_id", self.show_id)
    yield ("venue_id", self.venue_id)
    yield ("artist_id", self.artist_id)
    yield ("start_time", self.start_time)
    yield ("end_time", self.end_time)
    yield ("all_day", self.all_day)

  def __repr__(self):
    """
    """
    msg = "ShowObj item: \n"
    msg += "show_id: " + str(self.show_id) + "\n"
    msg += "venue_id: " + str(self.venue_id) + "\n"
    msg += "artist_id: " + str(self.artist_id) + "\n"
    msg += "start_time: " + str(self.start_time) + "\n"
    msg += "end_time: " + str(self.end_time) + "\n"
    msg += "all_day: " + str(self.all_day) + "\n"
    return msg

#----------------------------------------------------------------------------#
# Useful functions.
#----------------------------------------------------------------------------#

def sort_by_area(results, entity_type):
  """
  return object with search results seperated by city and state
  takes two parameters as input:
  - results (sqlalchemy search result of all Artists or Venues)
  - entity_type: specifies artist or venue search (string. "artists" if result
      is artist type and "venues" if result is venue type)
  returns a (nested) dict object with the following format:
  - keys "<area>": stored in the format "<city>, <state>".
  - values: dict with the following keys
      - obj[<area>]["city"] - city name
      - obj[<area>]["state"] - state name
      - obj[<city>, <state>]["artists"] || [<city>, <state>]["venues"]
  """
  areas = {}
  for result in results:
    area = result.city + ", " + result.state
    if area in areas:
      areas[area][entity_type].append(result)
    else:
      areas[area] = {"city": result.city,
                     "state": result.state,
                     entity_type: []}
  area_list = []
  for area in areas:
    area_list.append(areas[area])
  return area_list

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  """
  returns list of all venues
  """
  data = Venue.query.all()
  return render_template('pages/venues.html', data=data)

@app.route('/local_venues')
def local_venues():
  """
  returns list of venues, sorted by area
  """
  data = sort_by_area(Venue.query.all(), "venues")
  return render_template('pages/area_venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  """
  """
  search_term = request.form.get('search_term').strip()
  result = Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).all()
  data = {"search_term": search_term,
            "result": result}
  return render_template('pages/search_venues.html', data=data)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  """
  """
  venue = VenueObj().get_venue(venue_id).set_shows()
  print(venue)
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  """
  returns a list of all artists
  """
  data = Artist.query.all()
  return render_template('pages/artists.html', data=data)

@app.route('/local_artists')
def local_artists():
  """
  returns list of artists sorted by geographic location
  """
  data = sort_by_area(Artist.query.all(), "artists")
  return render_template('pages/artists.html', areas=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  """
  """
  search_term = request.form.get('search_term').strip()
  result = Artist.query.filter(Artist.name.ilike('%'+search_term+'%')).all()
  data = {"search_term": search_term,
            "result": result}
  return render_template('pages/search_artists.html', data=data)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  """
  shows the artist page with the given artist_id
  """
  artist = ArtistObj().get_artist(artist_id).set_shows()
  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(threaded=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
