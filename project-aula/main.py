"""`main` is the top level module for your Bottle application."""

# import the Bottle framework
from bottle import Bottle, debug
from google.appengine.ext import ndb
debug(True)
# Create the Bottle WSGI application.
bottle = Bottle()

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.



# Define an handler for the root URL of our application.
@bottle.route('/hello')
def hello():
	"""Return a friendly HTTP greeting."""
	return " Hello World!"

class MessageM(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


@bottle.route('/add/<s>')
def add(s):
	print "XXXXXX"
	m = MessageM(content = s)
	key = m.put()
	#return " x"
	return 'Message %s added with key %s' %(s, str(key.id()))


@bottle.route('/showall')
def showall():
	ret = ""
	msgs = MessageM.query()
	for m in msgs:
		ret += str(m.key.id()) + "    " +m.content + "     " +str(m.date) + "<br>"
	return ret 
@bottle.route('/showsome/<start:int>/<end:int>')
def showsome(start, end):
	ret = ""
	msgs = MessageM.query()
	for m in msgs.fetch(offset=start, limit=end-start):
		ret += str(m.key.id()) + "    " +m.content + "     " +str(m.date) + "<br>"
	return ret 

@bottle.route('/showexact/<string>')	
def showexact(string):
	ret = ""
	msgs = MessageM.query(Message.content==string)
	for m in msgs:
		ret += str(m.key.id()) + "    " +m.content + "     " +str(m.date) + "<br>"
	return ret 
	

# Define an handler for 404 errors.
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'
