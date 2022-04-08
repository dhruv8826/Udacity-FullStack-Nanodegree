#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# moved to seperate models.py
# had to move this import here otherwise was giving a circular import error
from models import *

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
	date = dateutil.parser.parse(value)
	if format == 'full':
			format="EEEE MMMM, d, y 'at' h:mma"
	elif format == 'medium':
			format="EE MM, dd, y h:mma"
	return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

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
	# TODO: replace with real venues data.
	#       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
	# data=[{
	#   "city": "San Francisco",
	#   "state": "CA",
	#   "venues": [{
	#     "id": 1,
	#     "name": "The Musical Hop",
	#     "num_upcoming_shows": 0,
	#   }, {
	#     "id": 3,
	#     "name": "Park Square Live Music & Coffee",
	#     "num_upcoming_shows": 1,
	#   }]
	# }, {
	#   "city": "New York",
	#   "state": "NY",
	#   "venues": [{
	#     "id": 2,
	#     "name": "The Dueling Pianos Bar",
	#     "num_upcoming_shows": 0,
	#   }]
	# }]

	data = []
	venues = Venue.query.all()
	areas = Venue.query.distinct(Venue.city, Venue.state).all()

	for area in areas:
		# print(area)
		venue_list = []
		for venue in venues:
			# print(venue)
			if (venue.city == area.city and venue.state == area.state):
				# print('inside loop-> ', venue)
				num_upcoming_shows=0
				shows = Show.query.filter_by(venue_id=venue.id).all()
				for show in shows:
					# print(show)
					if show.start_time > datetime.now():
						num_upcoming_shows += 1
				venue_list.append({
					"id": venue.id,
					"name": venue.name,
					"num_upcoming_shows": num_upcoming_shows
				})
				# print(venue_list)

		data.append({
			"city": area.city,
			"state": area.state,
			"venues": venue_list
		})
		print(data)
	return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
	# TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
	# seach for Hop should return "The Musical Hop".
	# search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
	# response={
	#   "count": 1,
	#   "data": [{
	#     "id": 2,
	#     "name": "The Dueling Pianos Bar",
	#     "num_upcoming_shows": 0,
	#   }]
	# }
	search_term = request.form.get('search_term', '')
	print('Search Term-> ',search_term)

	data = []
	venues_list = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
	print(venues_list)
	for venue in venues_list:
		upcoming_shows = []
		shows = Show.query.filter_by(venue_id=venue.id).all()
		for show in shows:
			if (show.start_time > datetime.now()):
				upcoming_shows.append(show)
		data.append({
			"id": venue.id,
			"name": venue.name,
			"num_upcoming_shows": len(upcoming_shows)
		})

	response = {
		"count": len(venues_list),
		"data": data
	}
	print(response)
	return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
	# shows the venue page with the given venue_id
	# TODO: replace with real venue data from the venues table, using venue_id
	# data1={
	#   "id": 1,
	#   "name": "The Musical Hop",
	#   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
	#   "address": "1015 Folsom Street",
	#   "city": "San Francisco",
	#   "state": "CA",
	#   "phone": "123-123-1234",
	#   "website": "https://www.themusicalhop.com",
	#   "facebook_link": "https://www.facebook.com/TheMusicalHop",
	#   "seeking_talent": True,
	#   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
	#   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
	#   "past_shows": [{
	#     "artist_id": 4,
	#     "artist_name": "Guns N Petals",
	#     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
	#     "start_time": "2019-05-21T21:30:00.000Z"
	#   }],
	#   "upcoming_shows": [],
	#   "past_shows_count": 1,
	#   "upcoming_shows_count": 0,
	# }
	# data2={
	#   "id": 2,
	#   "name": "The Dueling Pianos Bar",
	#   "genres": ["Classical", "R&B", "Hip-Hop"],
	#   "address": "335 Delancey Street",
	#   "city": "New York",
	#   "state": "NY",
	#   "phone": "914-003-1132",
	#   "website": "https://www.theduelingpianos.com",
	#   "facebook_link": "https://www.facebook.com/theduelingpianos",
	#   "seeking_talent": False,
	#   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
	#   "past_shows": [],
	#   "upcoming_shows": [],
	#   "past_shows_count": 0,
	#   "upcoming_shows_count": 0,
	# }
	# data3={
	#   "id": 3,
	#   "name": "Park Square Live Music & Coffee",
	#   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
	#   "address": "34 Whiskey Moore Ave",
	#   "city": "San Francisco",
	#   "state": "CA",
	#   "phone": "415-000-1234",
	#   "website": "https://www.parksquarelivemusicandcoffee.com",
	#   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
	#   "seeking_talent": False,
	#   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
	#   "past_shows": [{
	#     "artist_id": 5,
	#     "artist_name": "Matt Quevedo",
	#     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
	#     "start_time": "2019-06-15T23:00:00.000Z"
	#   }],
	#   "upcoming_shows": [{
	#     "artist_id": 6,
	#     "artist_name": "The Wild Sax Band",
	#     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
	#     "start_time": "2035-04-01T20:00:00.000Z"
	#   }, {
	#     "artist_id": 6,
	#     "artist_name": "The Wild Sax Band",
	#     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
	#     "start_time": "2035-04-08T20:00:00.000Z"
	#   }, {
	#     "artist_id": 6,
	#     "artist_name": "The Wild Sax Band",
	#     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
	#     "start_time": "2035-04-15T20:00:00.000Z"
	#   }],
	#   "past_shows_count": 1,
	#   "upcoming_shows_count": 1,
	# }
	# data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
	venue = Venue.query.get(venue_id)
	past_shows = []
	upcoming_shows = []

	# Using join as per review comments
	past_shows_details = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
	upcoming_shows_details = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).all()
	for past_show in past_shows_details:
		past_shows.append({
			'artist_id': past_show.artist_id,
			'artist_name': past_show.artist.name,
			'artist_image_link': past_show.artist.image_link,
			'start_time': format_datetime(str(past_show.start_time))
		})
	for upcoming_show in upcoming_shows_details:
		upcoming_shows.append({
			'artist_id': upcoming_show.artist_id,
			'artist_name': upcoming_show.artist.name,
			'artist_image_link': upcoming_show.artist.image_link,
			'start_time': format_datetime(str(upcoming_show.start_time))
		})

	# Old format without using join
	# shows = Show.query.filter_by(venue_id=venue_id).all()

	# for each_show in shows:
	#   if each_show.start_time > datetime.now():
	#     upcoming_shows.append({
	#       'artist_id': each_show.artist_id,
	#       'artist_name': each_show.artist.name,
	#       'artist_image_link': each_show.artist.image_link,
	#       'start_time': format_datetime(str(each_show.start_time))
	#     })
	#   else:
	#     past_shows.append({
	#       'artist_id': each_show.artist_id,
	#       'artist_name': each_show.artist.name,
	#       'artist_image_link': each_show.artist.image_link,
	#       'start_time': format_datetime(str(each_show.start_time))
	#     })
	
	data = {
		"id": venue.id,
		"name": venue.name,
		"genres": venue.genres.split(','),
		"address": venue.address,
		"city": venue.city,
		"state": venue.state,
		"phone": venue.phone,
		"website": venue.website_link,
		"facebook_link": venue.facebook_link,
		"seeking_talent": venue.looking_for_talent,
		"image_link": venue.image_link,
		"past_shows": past_shows,
		"upcoming_shows": upcoming_shows,
		"past_shows_count": len(past_shows),
		"upcoming_shows_count": len(upcoming_shows),
	}

	return render_template('pages/show_venue.html', venue=data)

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
	# flash('Venue ' + request.form['name'] + ' was successfully listed!')
	# TODO: on unsuccessful db insert, flash an error instead.
	# e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
	# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
	form = VenueForm()

	# Adding Validation
	if form.validate_on_submit():
		try:
			venue = Venue(
				name=form.name.data,
				city=form.city.data,
				state=form.state.data,
				address=form.address.data,
				phone=form.phone.data,
				image_link=form.image_link.data,
				facebook_link=form.facebook_link.data,
				website_link=form.website_link.data,
				looking_for_talent=form.seeking_talent.data,
				description=form.seeking_description.data,
				genres=form.genres.data
			)
			print(venue)
			
			db.session.add(venue)
			db.session.commit()
			flash('Venue ' + request.form['name'] + ' was successfully listed!')
		except:
			db.session.rollback()
			flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
		finally:
			db.session.close()
	else:
		for error in form.errors:
			flash('Error: ' + error)
	return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
	# TODO: Complete this endpoint for taking a venue_id, and using
	# SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

	# BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
	# clicking that button delete it from the db then redirect the user to the homepage
	venue = Venue.query.get(venue_id)
	if not venue:
		flash('No Venue with ID - ' + venue_id + 'exist.') 
	else:
		print(venue)
		try:
			db.session.delete(venue)
			db.session.commit()
			flash('Venue with ID - ' + venue_id + 'has been successfully deleted.')
			# print('inside try')
		except:
			db.session.rollback()
			flash('An error occured. Venue with ID - ' + venue_id + ' could not be deleted.')
			print('inside except')
		finally:
			db.session.close()
	
	return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
	# TODO: replace with real data returned from querying the database
	# data=[{
	#   "id": 4,
	#   "name": "Guns N Petals",
	# }, {
	#   "id": 5,
	#   "name": "Matt Quevedo",
	# }, {
	#   "id": 6,
	#   "name": "The Wild Sax Band",
	# }]
	data = []
	artists = Artist.query.all()

	for artist in artists:
		data.append({
			"id": artist.id,
			"name": artist.name
		})
	return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
	# TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
	# seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
	# search for "band" should return "The Wild Sax Band".
	# response={
	#   "count": 1,
	#   "data": [{
	#     "id": 4,
	#     "name": "Guns N Petals",
	#     "num_upcoming_shows": 0,
	#   }]
	# }
	search_term = request.form.get('search_term', '')
	print('Search Term-> ', search_term)

	data = []
	artists_list = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
	print(artists_list)
	for artist in artists_list:
		upcoming_shows = []
		shows = Show.query.filter_by(artist_id=artist.id).all()
		for show in shows:
			if (show.start_time > datetime.now()):
				upcoming_shows.append(show)
		data.append({
			"id": artist.id,
			"name": artist.name,
			"num_upcoming_shows": len(upcoming_shows)
		})

	response = {
		"count": len(artists_list),
		"data": data
	}
	print(response)
	return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
	# shows the artist page with the given artist_id
	# # TODO: replace with real artist data from the artist table, using artist_id
	# data1={
	#   "id": 4,
	#   "name": "Guns N Petals",
	#   "genres": ["Rock n Roll"],
	#   "city": "San Francisco",
	#   "state": "CA",
	#   "phone": "326-123-5000",
	#   "website": "https://www.gunsnpetalsband.com",
	#   "facebook_link": "https://www.facebook.com/GunsNPetals",
	#   "seeking_venue": True,
	#   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
	#   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
	#   "past_shows": [{
	#     "venue_id": 1,
	#     "venue_name": "The Musical Hop",
	#     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
	#     "start_time": "2019-05-21T21:30:00.000Z"
	#   }],
	#   "upcoming_shows": [],
	#   "past_shows_count": 1,
	#   "upcoming_shows_count": 0,
	# }
	# data2={
	#   "id": 5,
	#   "name": "Matt Quevedo",
	#   "genres": ["Jazz"],
	#   "city": "New York",
	#   "state": "NY",
	#   "phone": "300-400-5000",
	#   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
	#   "seeking_venue": False,
	#   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
	#   "past_shows": [{
	#     "venue_id": 3,
	#     "venue_name": "Park Square Live Music & Coffee",
	#     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
	#     "start_time": "2019-06-15T23:00:00.000Z"
	#   }],
	#   "upcoming_shows": [],
	#   "past_shows_count": 1,
	#   "upcoming_shows_count": 0,
	# }
	# data3={
	#   "id": 6,
	#   "name": "The Wild Sax Band",
	#   "genres": ["Jazz", "Classical"],
	#   "city": "San Francisco",
	#   "state": "CA",
	#   "phone": "432-325-5432",
	#   "seeking_venue": False,
	#   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
	#   "past_shows": [],
	#   "upcoming_shows": [{
	#     "venue_id": 3,
	#     "venue_name": "Park Square Live Music & Coffee",
	#     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
	#     "start_time": "2035-04-01T20:00:00.000Z"
	#   }, {
	#     "venue_id": 3,
	#     "venue_name": "Park Square Live Music & Coffee",
	#     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
	#     "start_time": "2035-04-08T20:00:00.000Z"
	#   }, {
	#     "venue_id": 3,
	#     "venue_name": "Park Square Live Music & Coffee",
	#     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
	#     "start_time": "2035-04-15T20:00:00.000Z"
	#   }],
	#   "past_shows_count": 0,
	#   "upcoming_shows_count": 3,
	# }
	# data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
	artist = Artist.query.get(artist_id)
	past_shows = []
	upcoming_shows = []

	# Using join as per review comments
	past_shows_details = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all()
	upcoming_shows_details = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()
	for past_show in past_shows_details:
		past_shows.append({
			"venue_id": past_show.venue_id,
			"venue_name": past_show.venue.name,
			"venue_image_link": past_show.venue.image_link,
			"start_time": format_datetime(str(past_show.start_time))
		})
	for upcoming_show in upcoming_shows_details:
		upcoming_shows.append({
			"venue_id": upcoming_show.venue_id,
			"venue_name": upcoming_show.venue.name,
			"venue_image_link": upcoming_show.venue.image_link,
			"start_time": format_datetime(str(upcoming_show.start_time))
		})

	# Old format without using join
	# shows = Show.query.filter_by(artist_id=artist_id).all()

	# for each_show in shows:
	#   if each_show.start_time > datetime.now():
	#     upcoming_shows.append({
	#       "venue_id": each_show.venue_id,
	#       "venue_name": each_show.venue.name,
	#       "venue_image_link": each_show.venue.image_link,
	#       "start_time": format_datetime(str(each_show.start_time))
	#     })
	#   else:
	#     past_shows.append({
	#       "venue_id": each_show.venue_id,
	#       "venue_name": each_show.venue.name,
	#       "venue_image_link": each_show.venue.image_link,
	#       "start_time": format_datetime(str(each_show.start_time))
	#     })
	
	data = {
		"id": artist.id,
		"name": artist.name,
		"genres": artist.genres.split(','),
		"city": artist.city,
		"state": artist.state,
		"phone": artist.phone,
		"seeking_venue": artist.looking_for_venues,
		"image_link": artist.image_link,
		"past_shows": past_shows,
		"upcoming_shows": upcoming_shows,
		"past_shows_count": len(past_shows),
		"upcoming_shows_count": len(upcoming_shows)
	}
	return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
	form = ArtistForm()
	artist_data = Artist.query.get(artist_id)
	# artist={
	#   "id": 1,
	#   "name": "Guns N Petals",
	#   "genres": ["Rock n Roll"],
	#   "city": "San Francisco",
	#   "state": "CA",
	#   "phone": "326-123-5000",
	#   "website": "https://www.gunsnpetalsband.com",
	#   "facebook_link": "https://www.facebook.com/GunsNPetals",
	#   "seeking_venue": True,
	#   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
	#   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
	# }
	artist={
		"id": artist_data.id,
		"name": artist_data.name,
		"genres": artist_data.genres,
		"city": artist_data.city,
		"state": artist_data.state,
		"phone": artist_data.phone,
		"website": artist_data.website_link,
		"facebook_link": artist_data.facebook_link,
		"seeking_venue": artist_data.looking_for_venues,
		"seeking_description": artist_data.description,
		"image_link": artist_data.image_link
	}
	print(artist)
	# TODO: populate form with fields from artist with ID <artist_id>
	return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
	# TODO: take values from the form submitted, and update existing
	# artist record with ID <artist_id> using the new attributes
	form = ArtistForm()
	try:
		artist = Artist.query.get(artist_id)

		artist.name = form.name.data
		artist.genres = form.genres.data
		artist.city = form.city.data
		artist.state = form.state.data
		artist.phone = form.phone.data
		artist.website_link = form.website_link.data
		artist.facebook_link = form.facebook_link.data
		artist.looking_for_venue = form.seeking_venue.data
		artist.description = form.seeking_description.data
		artist.image_link = form.image_link.data
		
		print('Updated Artist Detail - ', artist)
		db.session.commit()
		flash('Updated the Artist ' + form.name.data)
	except:
		db.session.rollback()
		flash('Something went wrong. Couldn\'t update Artist ' + form.name.data)
	finally:
		db.session.close()

	return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
	form = VenueForm()
	venue = Venue.query.get(venue_id)
	# venue={
	#   "id": 1,
	#   "name": "The Musical Hop",
	#   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
	#   "address": "1015 Folsom Street",
	#   "city": "San Francisco",
	#   "state": "CA",
	#   "phone": "123-123-1234",
	#   "website": "https://www.themusicalhop.com",
	#   "facebook_link": "https://www.facebook.com/TheMusicalHop",
	#   "seeking_talent": True,
	#   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
	#   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
	# }
	venue_data={
		"id": venue.id,
		"name": venue.name,
		"genres": venue.genres.split(','),
		"address": venue.address,
		"city": venue.city,
		"state": venue.state,
		"phone": venue.phone,
		"website": venue.website_link,
		"facebook_link": venue.facebook_link,
		"seeking_talent": venue.looking_for_talent,
		"seeking_description": venue.description,
		"image_link": venue.image_link
	}
	print(venue_data)
	# TODO: populate form with values from venue with ID <venue_id>
	return render_template('forms/edit_venue.html', form=form, venue=venue_data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
	# TODO: take values from the form submitted, and update existing
	# venue record with ID <venue_id> using the new attributes
	form = VenueForm()
	
	try:
		venue = Venue.query.get(venue_id)

		venue.name = form.name.data
		venue.genres = form.genres.data
		venue.address = form.address.data
		venue.city = form.city.data
		venue.state = form.state.data
		venue.phone = form.phone.data
		venue.website_link = form.website_link.data
		venue.facebook_link = form.facebook_link.data
		venue.looking_for_talent = form.seeking_talent.data
		venue.description = form.seeking_description.data
		venue.image_link = form.image_link.data

		print(venue)
		db.session.commit()
		flash('Updated details for Venue ' + form.name.data)
	except:
		db.session.rollback()
		flash('Something went wrong. Unable to update the Venue ' + form.name.data)
	finally:
		db.session.close()

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
	# flash('Artist ' + request.form['name'] + ' was successfully listed!')
	# TODO: on unsuccessful db insert, flash an error instead.
	# e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
	form = ArtistForm()

	# Adding Validation
	if form.validate_on_submit():	
		try:
			artist = Artist(
				name=form.name.data,
				city=form.city.data,
				state=form.state.data,
				phone=form.phone.data,
				genres=form.genres.data,
				image_link=form.image_link.data,
				facebook_link=form.facebook_link.data,
				website_link=form.website_link.data,
				looking_for_venues=form.seeking_venue.data,
				description=form.seeking_description.data
			)
			print(artist)

			db.session.add(artist)
			db.session.commit()
			flash('Artist ' + request.form['name'] + ' was successfully listed!')
		except:
			db.session.rollback()
			flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
		finally:
			db.session.close()
	else:
		for error in form.errors:
			flash('Error: ' + error)
	return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
	# displays list of shows at /shows
	# TODO: replace with real venues data.
	# data=[{
	#   "venue_id": 1,
	#   "venue_name": "The Musical Hop",
	#   "artist_id": 4,
	#   "artist_name": "Guns N Petals",
	#   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
	#   "start_time": "2019-05-21T21:30:00.000Z"
	# }, {
	#   "venue_id": 3,
	#   "venue_name": "Park Square Live Music & Coffee",
	#   "artist_id": 5,
	#   "artist_name": "Matt Quevedo",
	#   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
	#   "start_time": "2019-06-15T23:00:00.000Z"
	# }, {
	#   "venue_id": 3,
	#   "venue_name": "Park Square Live Music & Coffee",
	#   "artist_id": 6,
	#   "artist_name": "The Wild Sax Band",
	#   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
	#   "start_time": "2035-04-01T20:00:00.000Z"
	# }, {
	#   "venue_id": 3,
	#   "venue_name": "Park Square Live Music & Coffee",
	#   "artist_id": 6,
	#   "artist_name": "The Wild Sax Band",
	#   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
	#   "start_time": "2035-04-08T20:00:00.000Z"
	# }, {
	#   "venue_id": 3,
	#   "venue_name": "Park Square Live Music & Coffee",
	#   "artist_id": 6,
	#   "artist_name": "The Wild Sax Band",
	#   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
	#   "start_time": "2035-04-15T20:00:00.000Z"
	# }]
	data = []
	shows = Show.query.all()

	for show in shows:
		data.append({
			"venue_id": show.venue_id,
			"venue_name": show.venue.name,
			"artist_id": show.artist_id,
			"artist_name": show.artist.name,
			"artist_image_link": show.artist.image_link,
			"start_time": format_datetime(str(show.start_time))
		})
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
	# flash('Show was successfully listed!')
	# TODO: on unsuccessful db insert, flash an error instead.
	# e.g., flash('An error occurred. Show could not be listed.')
	# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
	form = ShowForm()

	try:
		show = Show(
			start_time=form.start_time.data,
			artist_id=form.artist_id.data,
			venue_id=form.venue_id.data
		)
		print(show)

		db.session.add(show)
		db.session.commit()
		flash('Show was successfully listed!')
	except:
		db.session.rollback()
		flash('An error occurred. Show could not be listed.')
	finally:
		db.session.close()
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
		app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
		port = int(os.environ.get('PORT', 5000))
		app.run(host='0.0.0.0', port=port)
'''
