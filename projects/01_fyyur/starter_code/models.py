from app import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(300))
    looking_for_talent = db.Column(db.Boolean)
    description = db.Column(db.String)
    genres = db.Column(db.String(200))

    def __repr__(self):
        return f'<Venue ID: {self.id}, Name: {self.name}, City: {self.city}, State: {self.state}, Address: {self.address}, Phone: {self.phone}, Image Link: {self.image_link}, Facebook Link: {self.facebook_link}, Website Link: {self.website_link}, Looking For Talent: {self.looking_for_talent}, Description: {self.description}, Genres: [{self.genres}]>'


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(200))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(300))
    looking_for_venues = db.Column(db.Boolean)
    description = db.Column(db.String)

    def __repr__(self):
        return f'<Artist ID: {self.id}, Name: {self.name}, City: {self.city}, State: {self.state}, Phone: {self.phone}, Image Link: {self.image_link}, Facebook Link: {self.facebook_link}, Website Link: {self.website_link}, Looking For Venue: {self.looking_for_venues}, Description: {self.description}, Genres: [{self.genres}]>'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())
    
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    artist = db.relationship('Artist', backref='show')
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    venue = db.relationship('Venue', backref='show')

    def __repr__(self):
        return f'<Show ID: {self.id}, Start Time: {self.start_time}, Artist ID: {self.artist_id}, Venue ID: {self.venue_id}>'
