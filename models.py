from google.appengine.ext import ndb

class Message(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    nachricht = ndb.TextProperty()