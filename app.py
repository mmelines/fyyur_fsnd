#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from unicodedata import name
import dateutil.parser
import babel
import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from model import *
from pprint import pprint

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db.app = app
db.init_app(app)
migrate = Migrate(app, db)
db.create_all()

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
    self.genres = False
    self.shows = None #TODO
    self.past_shows = None #TODO
    self.upcoming_shows = None #TODO
    self.genre_string = None #TODO
    self.json = None

  def copy(self, obj):
    """
    populate entity with data from a SQLAlchemy object
    """
    if hasattr(obj, 'id'):
      self.id = obj.id
    if hasattr(obj, 'name'):
      self.name = obj.name
    if hasattr(obj, 'state'):
      self.state = obj.state
    if hasattr(obj, 'city'):
      self.city = obj.city
    if self.entity_type=="venue" and hasattr(obj, 'address'):
      self.address = obj.address
    if hasattr(obj, 'phone'):
      self.phone = obj.phone
    if hasattr(obj, 'image_link'):
      self.image_link = obj.image_link
    if hasattr(obj, 'facebook_link'):
      self.facebook_link = obj.facebook_link
    if hasattr(obj, 'genres'):
      self.genres = obj.genres
    if hasattr(obj, 'is_seeking'):
      self.is_seeking = obj.is_seeking
    if hasattr(obj, 'website_link'):
      self.website_link = obj.website_link
    if hasattr(obj, 'seeking_description'):
      self.seeking_description = obj.seeking_description
    if hasattr(obj, 'has_image'):
      self.has_image = obj.has_image
    self.list_genres()
    self.json = self.return_json()
    return self

  def return_json(self):
    """
    return dict of entity based on fields populated in SQLAlchemy object
    """
    json_dict = {}
    for item in self:
      json_dict[item[0]] = item[1]
    self.json = json_dict
    return json_dict

  def list_genres(self):
    """
    modify genres attribute in json object to contain list of genres as
    opposed to the genre_string, seperated by commas
    """
    if isinstance(self.genres, str):
      genres = self.genres
      self.genre_string = genres
      self.genres = genres.split(',')

  def format_genres(self, genres_list):
    """
    fomat genres from list into string stored in db
    used to evaluate if genres have been modified in an update
    """
    form_genres = genres_list.split(", ")
    altered_genres = []
    genre_confirm = [""]*len(self.genres)
    plausable = True # remains true while it is plausable genres remain unchanged
    for form_genre_name in form_genres:
      print(form_genre_name)
      altered_genres.append(form_genre_name)
      if not form_genre_name in self.genres:
        plausable = False
      if form_genre_name in self.genres and plausable == True:
        genre_confirm[self.genres.index(form_genre_name)] = form_genre_name
    if plausable == False or "" in genre_confirm:
      self.genres = altered_genres
      genre_string = ""
      for final_genre in altered_genres:
        genre_string += final_genre + ","
      self.genre_string = genre_string[:-1]
      plausable = False
    return not plausable

  def create_edit(self, form):
    """
    alter sqlalchemy object to update database
    and attempt to commit the update if changes were made
    """
    if self.entity_type == "artist":
      entity = Artist.query.get(self.id)
    elif self.entity_type == "venue":
      entity = Venue.query.get(self.id)
    updates = 0
    # if user has made changes for an update, add them to session entity obj
    # count how many updates have been made
    if 'name' in form:
      if str(self.name) != str(form.get('name')):
        entity.name = form.get('name')
        updates += 1
    if 'state' in form:
      if str(self.state) != str(form.get('state')):
        entity.state = form.get('state')
        updates += 1
    if 'city' in form:
      if str(self.city) != str(form.get('city')):
        entity.city = form.get('city')
        updates += 1
    if 'address' in form:
      if str(self.address) != str(form.get('address')):
        entity.address = form.get('address')
        updates += 1
    if 'phone' in form:
      if str(self.phone) != str(form.get('phone')):
        entity.phone = form.get('phone')
        updates += 1
    if 'image_link' in form:
      if str(self.image_link) != str(form.get('image_link')):
        entity.image_link = form.get('image_link')
        updates += 1
    if 'facebook_link' in form:
      if str(self.facebook_link) != str(form.get('facebook_link')):
        entity.facebook_link = form.get('facebook_link')
        updates += 1
    if 'genres' in form:
      genres_control = self.format_genres(form.get('genres_string'))
      if genres_control == True:
        entity.genres = self.genre_string
        updates += 1
    if 'is_seeking' in form:
      if str(self.is_seeking) != str(form.get('is_seeking')):
        entity.is_seeking = form.get('is_seeking')
        updates += 1
    if 'website_link' in form:
      if str(self.website_link) != str(form.get('website_link')):
        entity.website_link = form.get('website_link')
        updates += 1
    if 'seeking_description' in form:
      if str(self.seeking_description) != str(form.get('seeking_description')):
        entity.seeking_description = form.get('seeking_description')
        updates += 1
    has_image = True if 'has_image' in form else False
    if has_image != self.has_image:
      entity.has_image = has_image
      updates += 1
    # if any changes were made, commit the entity session object to database
    if updates > 0:
      try:
        db.session.commit()
        status_code = 201
        error = False
        name = entity.name
      except (BaseException, SQLAlchemyError) as err:
        db.session.rollback()
        status_code = 409
        name = ""
        error = err
        print(err)
      except:
        db.session.rollback()
        status_code = 409
        name = ""
        error = True
      finally:
        status = {"verb": "edited",
                "status": status_code,
                  "error": error}
        if len(name) > 0:
          status["name"] = name
    else:
      status = {"verb": "edited",
                "status": 200,
                "error": False}
    return status
  
  def create_insert(self, entity_type, form):
    """

    """
    not_recieved = []
    if entity_type == "artist":
      entity = Artist()
    if entity_type == "venue":
      entity = Venue()
    try:
      entity.name = request.form.get('name')
    except:
      not_recieved.append("name")
    try:
      entity.state = request.form.get('state')
    except:
      not_recieved.append("state")
    try:
      entity.city = request.form.get('city')
    except:
      not_recieved.append("city")
    try:
      entity.address = request.form.get('address')
    except:
      not_recieved.append("address")
    try:
      entity.phone = request.form.get('phone')
    except:
      not_recieved.append("phone")
    try:
      entity.image_link = request.form.get('image_link')
    except:
      not_recieved.append("image_link")
    try:
      entity.facebook_link = request.form.get('facebook_link')
    except:
      not_recieved.append("facebook_link")
    try:
      entity.genres = request.form.get('genres')
    except:
      not_recieved.append("genres")
    try:
      entity.is_seeking = request.form.get('is_seeking')
    except:
      not_recieved.append("is_seeking")
    try:
      entity.website_link = request.form.get('website_link')
    except:
      not_recieved.append("website_link")
    try:
      entity.seeking_description = request.form.get('seeking_description')
    except:
      not_recieved.append("seeking_description")
    try:
      entity.has_image = request.form.get('has_image')
    except:
      not_recieved.append("has_image")
    # attempt to commit new object to database
    try:
      db.session.add(entity)
      db.session.commit()
      status = {"status": 200,
                "error": False,
                "name": request.form.get('name'),
                "id": entity.id}
    except (BaseException, SQLAlchemyError) as err:
      # if a common error occurs, print error and set code to 409
      db.session.rollback()
      status_code = 409
      name = ""
      error = err
      print(err)
    except:
      # if an error occurs outside of base classes, catch it anyways
      db.session.rollback
      status = {"status": 409,
                "error": True}
    finally:
      status["verb"] = "listed"
      return status
  
  def __iter__(self):
    """
    define iterator properties of generic object
    """
    yield ("id", self.id)
    yield ("name", self.name)
    yield ("state", self.state)
    yield ("city", self.city)
    yield ("phone", self.phone)
    if hasattr(self, 'address'):
      yield("address", self.address)
    yield ("image_link", self.image_link)
    yield ("facebook_link", self.facebook_link)
    yield ("genres", self.genres)
    yield ("is_seeking", self.is_seeking)
    yield ("seeking_description", self.seeking_description)
    yield ("has_image", self.has_image)
    yield ("shows", self.shows)
    yield ("past_shows", self.past_shows)
    yield ("upcoming_shows", self.upcoming_shows)

  def __repr__(self):
    """
    define string representation of entity instance
    """
    msg = "id: " + str(self.id) + "; "
    msg += "name: " + str(self.name) + "\n"
    msg += "state: " + str(self.state) + "\n"
    msg += "city: " + str(self.city) + "\n"
    msg += "phone: " + str(self.phone) + "\n"
    msg += "image_link: " + str(self.image_link) + "\n"
    msg += "facebook_link: " + str(self.facebook_link) + "\n"
    msg += "genres: " + str(self.genres) + "\n"
    msg += "is_seeking: " + str(self.is_seeking) + "\n"
    msg += "seeking_description: " + str(self.seeking_description) + "\n"
    msg += "has_image: " + str(self.has_image) + "\n"
    msg += "shows: " + str(self.shows) + "\n"
    return msg

  def flash(self, obj):
    """
    generate messages to be flashed in common situations
    """
    if not obj is None:
      if "name" in obj.keys():
        if obj["error"] == False:
          msg = self.entity_type + " " + obj["name"] + " was " + obj["verb"] + " successfully."
        else:
            msg = "Oops! Something went wrong on our end. "
            if obj["name"] != False:
              msg += self.entity_type + " " + obj["name"] + " could not be " + obj["verb"] + ". "
            msg += "Please try again later."
      else:
        msg = "Could not create " + self.entity_type + ". Invalid Form submission."
    else:
      msg = "Error. Form not recieved."
    obj["flash_msg"] = msg
    print("--------------- ** FLASH ** ---------------")
    print(obj)
    print("---------------    click    ---------------")
    return obj

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
    """
    get all shows associated to an artist or venue as a list
    """
    if self.entity_type == "artist":
      shows = Show.query.filter_by(artist_id=self.id).all()
    if self.entity_type == "venue":
      shows = Show.query.filter_by(venue_id=self.id).all()
    return shows

  def set_shows(self):
    """
    append show dict (neccessary display information) to existing entity object
    """
    def append_pair(show, entity_type):
      """
      append the name and image dict "paried" to the show id
      seperate past and upcoming shows
      """
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
      # get neccessary information to display show from id in shows list
      # append it to self.shows dict or, if it does not exist, create it
      new_show = append_pair(ShowObj().copy(show), self.entity_type)
      if self.shows is None:
        self.shows = {new_show.show_id : new_show}
      else:
        if not new_show.show_id in self.shows.keys():
          self.shows[new_show.show_id] = new_show
      # seperate past and upcoming shows
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
  Handles common functions of Artist object formatting
  """

  def __init__(self, **kwargs):
    """
    init instance of ArtistObj class
    """
    super().__init__() #inherit entity base class
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
    artist.id = artist_id;
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
    status = self.create_insert("artist", form)
    data = self.flash(status)
    return data

  def edit_artist(self, obj):
    """
    generate artist edit based on form input
    if error, direct to handle_error() before returning

    takes two input parameters:
    - artist: original artist object with given data
    - form: response of POST request
    returns status (boolean). True if success and False if failure
    """
    pprint(obj)
    status = self.create_edit(obj)
    data = self.flash(status)
    return data
  
  def set_avail(self):
    try:
      avail = ArtistAvail.query.get(self.id)
      strs = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", 
        "Saturday"]
      chars = ["U", "M", "T", "W", "R", "F", "S"]
      i = 0
      week = {}
      for str in strs:
        day = {"name": str,
              "abbr": chars[i]}
        week[i] = day
        i += 1
      week[0]["value"] = avail.sun
      week[1]["value"] = avail.mon
      week[2]["value"] = avail.tue
      week[3]["value"] = avail.wed
      week[4]["value"] = avail.thu
      week[5]["value"] = avail.fri
      week[6]["value"] = avail.sat
    except: 
      week = {0: False}
    artist = self.return_json()
    artist["availability"] = week
    return artist

class VenueObj(Obj):
  """
  Handles common functions of Venue object formatting
  """

  def __init__(self, **kwargs):
    """
    init instance of Venue class
    """
    super().__init__() #init entity base clase
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
    status = self.create_insert("venue", form)
    data = self.flash(status)
    return data

  def edit_venue(self, obj):
    """
    generate venue edit based on form input
    if error, direct to handle_error() before returning
    takes two input parameters:
    - venue: original venue object with given data
    - form: response of POST request
    returns status (boolean). True if success and False if failure
    """
    status = self.create_edit(obj)
    data = self.flash(status)
    return data

class ShowObj:
  """
  handles common functions of ShowObj formatting
  """

  def __init__(self):
    """
    init instance of class ShowObj
    """
    self.show_id = None
    self.venue_id = None
    self.artist_id = None
    self.start_time = None
    self.start = {}
    self.end_time = None
    self.end = {}
    self.all_day = None
    self.artist_image_link = None
    self.venue_name = None
    self.venue_image_link = None
    self.venue_name = None
    self.json = {}

  def create_insert(self, form):
    """
    insert show object
    """
    not_recieved = []
    show = Show()
    try:
      show.name = request.form.get('show_id')
    except:
      not_recieved.append("show_id")
    try:
      show.venue_id = request.form.get('venue_id')
    except:
      not_recieved.append("venue_id")
    try:
      show.artist_id = request.form.get('artist_id')
    except:
      not_recieved.append("artist_id")
    try:
      show.start_time = request.form.get('start_time')
    except:
      not_recieved.append("start_time")
    try:
      show.end_time = request.form.get('end_time')
    except:
      not_recieved.append("end_time")
    try:
      show.all_day = request.form.get('all_day')
    except:
      not_recieved.append("all_day")
    try:
      db.session.add(show)
      db.session.commit()
      status = {"status": 200,
                "error": False,
                "id": show.id}
    except (BaseException, SQLAlchemyError) as err:
      db.session.rollback()
      status_code = 409
      name = ""
      error = err
      print(err)
    except:
      db.session.rollback
      status = {"status": 409,
                "error": True}
    finally:
      status["verb"] = "listed"
      print(" -- status in create_show: ")
      print(status)
      return status

  def create_edit(self, form):
    """
show_id
venue_id
artist_id
start_time
end_time
all_day
    """
    show = Show.query.get(self.id)
    updates = 0
    if 'show_id' in form:
      print("found show_id in form: " + str(form.get('show_id')))
      if str(self.show_id) != str(form.get('show_id')):
        print(" >> no match; updating self.show_id to " + str(form.get('show_id')))
        show.show_id = form.get('show_id')
        updates += 1
      else:
        print(" >> matches; skipping")
    if 'venue_id' in form:
      print("found venue_id in form: " + str(form.get('venue_id')))
      if str(self.venue_id) != str(form.get('venue_id')):
        print(" >> no match; updating self.venue_id to " + str(form.get('venue_id')))
        show.venue_id = form.get('venue_id')
        updates += 1
      else:
        print(" >> matches; skipping")
    if 'artist_id' in form:
      print("found artist_id in form: " + str(form.get('artist_id')))
      if str(self.artist_id) != str(form.get('artist_id')):
        print(" >> no match; updating self.artist_id to " + str(form.get('artist_id')))
        show.artist_id = form.get('artist_id')
        updates += 1
      else:
        print(" >> matches; skipping")
    if 'start_time' in form:
      print("found start_time in form: " + str(form.get('start_time')))
      if str(self.start_time) != str(form.get('start_time')):
        print(" >> no match; updating self.start_time to " + str(form.get('start_time')))
        show.start_time = form.get('start_time')
        updates += 1
      else:
        print(" >> matches; skipping")
    if 'end_time' in form:
      print("found end_time in form: " + str(form.get('end_time')))
      if str(self.end_time) != str(form.get('end_time')):
        print(" >> no match; updating self.end_time to " + str(form.get('end_time')))
        show.end_time = form.get('end_time')
        updates += 1
      else:
        print(" >> matches; skipping")
    if 'all_day' in form:
      print("found all_day in form: " + str(form.get('all_day')))
      if str(self.all_day) != str(form.get('all_day')):
        print(" >> no match; updating self.all_day to " + str(form.get('all_day')))
        show.all_day = form.get('all_day')
        updates += 1
      else:
        print(" >> matches; skipping")
    if updates > 0:
      try:
        db.session.commit()
        status_code = 201
        error = False
        name = show.name
      except (BaseException, SQLAlchemyError) as err:
        db.session.rollback()
        status_code = 409
        name = ""
        error = err
        print(err)
      except:
        db.session.rollback()
        status_code = 409
        name = ""
        error = True
      finally:
        status = {"verb": "edited",
                "status": status_code,
                  "error": error}
        if len(name) > 0:
          status["name"] = name
    else:
      status = {"verb": "edited",
                "status": 200,
                "error": False}
    return status

  def copy(self, obj):
    """
    populate ShowObj item from SQLAlchemy object
    """
    def expand_datetime(show_date):
      print("called expand_datetime " + str(show_date) + " (" + str(type(show_date)) + ")")
      """
      datetime = {"year": show_date.year,
                  "month": show_date.month,
                  "day": show_date.,
                  "hour": ,
                  "minute": ,
                  "second": ,}
      """

    if hasattr(obj, 'show_id'):
      self.show_id = obj.show_id
    if hasattr(obj, 'venue_id'):
      self.venue_id = obj.venue_id
    if hasattr(obj, 'artist_id'):
      self.artist_id = obj.artist_id
    if hasattr(obj, 'start_time'):
      self.start_time = obj.start_time
      expand_datetime(self.start_time)
    if hasattr(obj, 'end_time'):
      self.end_time = obj.end_time
      expand_datetime(self.end_time)
    if hasattr(obj, 'all_day'):
      self.all_day = obj.all_day
    json_dict = {}
    for item in self:
      print(item)
      json_dict[item[0]] = item[1]
    self.json = json_dict
    return self

  def __iter__(self):
    """
    define iterative properties of ShowObj class
    """
    yield ("show_id", self.show_id)
    yield ("venue_id", self.venue_id)
    yield ("artist_id", self.artist_id)
    yield ("start_time", self.start_time)
    yield ("end_time", self.end_time)
    yield ("all_day", self.all_day)

  def __repr__(self):
    """
    define string representation of ShowObj instances
    """
    msg = "ShowObj item: \n"
    msg += "show_id: " + str(self.show_id) + "\n"
    msg += "venue_id: " + str(self.venue_id) + "\n"
    msg += "artist_id: " + str(self.artist_id) + "\n"
    msg += "start_time: " + str(self.start_time) + "\n"
    msg += "end_time: " + str(self.end_time) + "\n"
    msg += "all_day: " + str(self.all_day) + "\n"
    return msg

class AvailObj():
  """
  handles common functions for ArtistAvail() functionality
  """

  def __init__(self):
    """
    init instance of artist avail obj
    """
    self.id = False
    self.sun = None
    self.mon = None
    self.tue = None
    self.wed = None
    self.thu = None
    self.fri = None
    self.sat = None
    self.week = None

  def __iter__(self):
    """
    iter property of artist avail obj
    """
    yield ("id", self.id)
    yield ("sun", self.sun)
    yield ("mon", self.mon)
    yield ("tue", self.tue)
    yield ("wed", self.wed)
    yield ("thu", self.thu)
    yield ("fri", self.fri)
    yield ("sat", self.sat)
  
  def set(self, artist_id):
    """
    set values of object to result of query
    """
    artist = ArtistAvail.query.get(artist_id)
    self.id = artist.id
    self.sun = artist.sun
    self.mon = artist.mon
    self.tue = artist.tue
    self.wed = artist.wed
    self.thu = artist.thu
    self.fri = artist.fri
    self.sat = artist.sat
    self.week = self.form_week()
  
  def edit(self, list):
    """
      compare sqlalchemy object from a list of t/f values to existing
        object from query
      updates only the changed values
      returns sqlalchemy object if any changes were made else False
    """
    updates = 0
    artist = ArtistAvail()
    if len(list) == 7:
      if (self.sun != list[0]):
        self.sun = list[0]
        artist.sun = list[0]
        updates += 1
      if (self.mon != list[1]):
        self.mon = list[1]
        artist.mon = list[1]
        updates += 1
      if (self.tue != list[2]):
        self.tue = list[2]
        artist.tue = list[2]
        updates += 1
      if (self.wed != list[3]):
        self.wed = list[3]
        artist.wed = list[3]
        updates += 1
      if (self.thu != list[4]):
        self.thu = list[4]
        artist.thu = list[4]
        updates += 1
      if (self.fri != list[5]):
        self.fri = list[5]
        artist.thu = list[5]
        updates += 1
      if (self.sat != list[6]):
        self.sat = list[6]
        artist.fri = list[6]
        updates += 1
    if updates > 0:
      return artist
    else:
      return False
  
  def copy(self, artist_id, list):
    """
    create sqlalchemy object from a list of t/f values
    updates self
    returns sqlalchemy object
    """
    artist = ArtistAvail()
    if len(list) == 7:
      artist.id = artist_id
      self.sun = list[0]
      artist.sun = list[0]
      self.mon = list[1]
      artist.mon = list[1]
      self.tue = list[2]
      artist.tue = list[2]
      self.wed = list[3]
      artist.wed = list[3]
      self.thu = list[4]
      artist.thu = list[4]
      self.fri = list[5]
      artist.fri = list[4]
      self.sat = list[6]
      artist.sat = list[6]
    return artist
  
  def form_week(self):
    return [self.sun, self.mon, self.tue, self.wed, self.thu, self.fri, 
      self.sat, self.sun]
  
#----------------------------------------------------------------------------#
# Useful functions.
#----------------------------------------------------------------------------#
def expand_shows():
  """
  expand ShowObj to contain artist and venue information for display
  """
  shows = Show.query.all()
  show_dict = {"artists": {}, "venues": {}}
  expanded_shows = []
  for sqlalchemy_show in shows:
    show = ShowObj().copy(sqlalchemy_show)
    # get artist information from artist_id
    show_artist_id = show.artist_id
    # if artist not already stored, query db for artist based on id information
    #  reduces n queries if multiple shows exist for an artist entry
    if not show_artist_id in show_dict["artists"]:
      sqlalchemy_artist = Artist.query.get(show_artist_id)
      show_artist = ArtistObj().copy(sqlalchemy_artist)
      show_dict["artists"][show_artist_id] = {}
      show_dict["artists"][show_artist_id]["image_link"] = show_artist.image_link
      show_dict["artists"][show_artist_id]["name"] = show_artist.name
    # copy information from show_dict to show obj for display
    show.artist_image_link = show_dict["artists"][show_artist_id]["image_link"]
    show.artist_name = show_dict["artists"][show_artist_id]["name"]
    # get venue information from venue_id
    show_venue_id = show.venue_id
    # if venue not already stored, query db for venue based on id information
    #  reduces n queries if multiple show exist for one venue entity
    if not show_venue_id in show_dict["venues"]:
      sqlalchemy_venue = Venue.query.get(show_venue_id)
      show_venue = VenueObj().copy(sqlalchemy_venue)
      show_dict["venues"][show_venue_id] = {}
      show_dict["venues"][show_venue_id]["image_link"] = show_venue.image_link
      show_dict["venues"][show_venue_id]["name"] = show_venue.name
    # copy information from show_dict to show object
    show.venue_image_link = show_dict["venues"][show_venue_id]["image_link"]
    show.venue_name = show_dict["venues"][show_venue_id]["name"]
    # add expanded show dict to list of expanded shows
    expanded_shows.append(show)
  return expanded_shows

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
    # generate unique location header for search
    area = result.city + ", " + result.state
    if area in areas:
      areas[area][entity_type].append(result)
    else:
      areas[area] = {"city": result.city,
                     "state": result.state,
                     entity_type: []}
  # generate list of search results and their headers
  area_list = []
  for area in areas:
    area_list.append(areas[area])
  return area_list

def json_genres():
  """
  get all genres
  """
  genres = Genre.query.all()
  json_obj = {}
  for genre in genres:
    json_obj[str(genre.id)] = {"name": genre.name}
  return json_obj

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
  returns list of venues, sorted by area
  """
  data = sort_by_area(Venue.query.all(), "venues")
  return render_template('pages/area_venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  """
  returns search result for venue search
  """
  search_term = request.form.get('search_term').strip()
  result = Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).all()
  data = {"search_term": search_term,
            "result": result}
  return render_template('pages/search_venues.html', data=data)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  """
  returns details for individual venue
  """
  venue = VenueObj().get_venue(venue_id).set_shows()
  print(venue)
  return render_template('pages/show_venue.html', venue=venue)

@app.route('/venues/<venue_id>/verify')
def verify_venue(venue_id):
  """
  verifies venue id exists in database
  """
  verified_venue = Venue.query.get(venue_id)
  try:
    verification = {"name": verified_venue.name,
                    "img": verified_venue.image_link}
  except:
    verification = {"name": False}
  print("hit " + str(venue_id) + " with a " + str(verification))
  return jsonify(verification)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  """
  return form to create genre
  """
  form = VenueForm()
  genres = json_genres()
  return render_template('forms/new_venue.html', form=form, genres=genres)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  """
  recieve create genre form content as POST and commit it to database
  """
  data = VenueObj().form_venue(request.form)
  flash(data["flash_msg"])
  return redirect(url_for('venues'))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  print("hit delete_venue")
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # return None

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
  returns values from a search of artist names
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
  artist = ArtistObj().get_artist(artist_id)
  artist = artist.set_shows()
  artist = artist.set_avail()
  return render_template('pages/show_artist.html', artist=artist)

@app.route('/artists/<artist_id>/verify')
def verify_artist(artist_id):
  """
  validates artist id is valid
  """
  try:
    verified_artist = Artist.query.get(artist_id)
    verification = {"name": verified_artist.name,
                    "img": verified_artist.image_link}
  except:
    verification = {"name": False}
  print("hit " + str(artist_id) + " with a " + str(verification))
  return jsonify(verification)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  """
  return artist edit form populated with current artist data
  """
  artist = ArtistObj().get_artist(artist_id)
  artist = artist.set_avail()
  form = ArtistForm()
  genres = json_genres()
  return render_template('forms/edit_artist.html', form=form, artist=artist, 
    genres=genres)

@app.route('/artists/<artist_id>/edit', methods=["POST"])
def edit_artist_submission(artist_id):
  """
  recieve artist update info as POST and commit it to database
  """
  artist = ArtistObj().get_artist(artist_id)
  data = artist.edit_artist(request.form)
  flash(data["flash_msg"])
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  """
  return venue edit form populated with current venue data
  """
  venue = VenueObj().get_venue(venue_id)
  form = VenueForm()
  genres = json_genres()
  return render_template('forms/edit_venue.html', form=form, venue=venue, genres=genres)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  """
  recieve artist edit form as POST and commit it to database
  """
  venue = VenueObj().get_venue(venue_id)
  data = venue.edit_venue(request.form)
  flash(data["flash_msg"])
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  """
  render new artist form
  """
  form = ArtistForm()
  genres = json_genres()
  return render_template('forms/new_artist.html', form=form, genres=genres)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  """
  recieve information for new artist as POST and commit it to database
  """
  data = ArtistObj().form_artist(request.form)
  flash(data["flash_msg"])
  return redirect(url_for('artists'))

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  """
  display all shows
  """
  data = expand_shows()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  """
  render create_shows form
  """
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
  # return render_template('pages/home.html')
  return redirect(url_for('create_shows'))

#  Error Handling
#  ----------------------------------------------------------------

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
