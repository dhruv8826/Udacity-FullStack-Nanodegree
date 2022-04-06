import sys
from app import Venue, Artist, Show
print (sys.path)

print (Venue.query.all())

print (Artist.query.all())

print (Show.query.all())