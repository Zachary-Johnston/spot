from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import Response
from spotipy import Spotify

from pyramid.httpexceptions import HTTPFound            # Perform redirects from the backend to other routes
# NOTE: this is unencrypted but signed session stored in client cookies. It isn't the most secure, but at least it's baked into Pyramid. Shame on Pyramid!
from pyramid.session import SignedCookieSessionFactory  # The default session factory to generate session objects

import mysql.connector as mysql
import requests
import json
import os
import time
import paho.mqtt.client as mqtt
import spotipy
import spotipy.util as util


db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']





def spotify(req):
  return render_to_response('templates/spotify.html', {}, request =req)

def get_playlists(req):
    ## Authentication
  # Register an app with https://developer.spotify.com/dashboard/ and paste your Client ID and Client Secret on the line below
  token = util.oauth2.SpotifyClientCredentials(client_id='531bf1de1dc44e71bd4bb4f9c69af7a7', client_secret='0d6921a912534d15b5fed7e75b4f46b2')
  cache_token = token.get_access_token()
  spotify = spotipy.Spotify(cache_token)

  # Get the first 100 (max) songs in the playlist
  results = spotify.user_playlist_tracks('spotify:user:zack_johnston', 'spotify:playlist:6dosGTCTRJ5xtA3XM6YTZb', limit=100, offset=0)

  # Store results in a tracks array
  tracks = results['items']
  #print(json.dumps(results))
  #new_adds = []
  records = {}
  records = Response(body=json.dumps(results))
  records.headers.update({'Access-Control-Allow-Origin': '*',})
  return records


  # Continue paginating through until all results are returned
  #while results['next']:
    #results = spotify.next(results)
    #tracks.extend(results['items'])
    #for items in (tracks):
    #new_adds.append(item['name'])

  #print(json.dumps(new_adds))

  #print(json.dumps(track['artists'][0]['name']))
  #print(json.dumps(track['artists']))
  #print(json.dumps(track['artists']['name']))

# Route to retrieve the login page
def login(req):
  error = req.session.pop_flash('login_error')
  error = error[0] if error else ''
  return render_to_response('templates/login.html', {'error': error})

# Route to retrieve the LOGGED-IN homepage
def get_home(req):
  if 'user' in req.session: # logged in
    return render_to_response('templates/portal.html',{'user':req.session['user']})
  else: # not logged in
    return HTTPFound(req.route_url("login"))
  


# Route to handle login form submissions coming from the login page
def post_login(req):
  email = None
  password = None
  if req.method == "POST":
    email = req.params['Email']
    password = req.params['Password']

  # Connect to the database and try to retrieve the user
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  query = "SELECT Email, Password FROM Users WHERE Email='%s';" % email 
  cursor.execute(query)
  user = cursor.fetchone() # will return a tuple (email, password) if user is found and None otherwise
  db.close()

  # If user is found and the password is valid, store in session, and redirect to the homepage
  # Otherwise, redirect back to the login page with a flash message
  # Note: passwords should be hashed and encrypted in actual production solutions!
  if user is not None and user[1] == password: 
    req.session['user'] = user[0] # set the session variable
    return HTTPFound(req.route_url("get_home"))
  else:
    req.session.invalidate() # clear session
    req.session.flash('Invalid login attempt. Please try again.', 'login_error')
    return HTTPFound(req.route_url("login"))


  
  
  












def coffeeset(req):
  # View the Dictionary that was Posted
  # Get the fname
  print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
  info = req.json_body
  print(info)

  msg = json.dumps(info)
  print(msg)
  
  records = {}
  records['success'] = True
  records = Response(body=json.dumps(records))
  records.headers.update({'Access-Control-Allow-Origin': '*',})

  return records

#def coffeeset(req):
 # View the Dictionary that was Posted
 # Get the fname
 #print("bbbeeeeeppppp")
 #temp = str(req.params.getall("temperature"))
 # Get rid of the [] that comes from req
 #print(temp)
 #start = time.time()
 #print(start)
 #temp = temp[2:len(temp)-2]
 #print(temp)
 #db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
 #cursor = db.cursor()
 # Insert Records
 #query = "insert into cofset (coffeeid, temperature, time) values (%s, %s, %s)"
 #values = [
 #("testid", temp, start),
 #]
 #print("GOT THIS FAR1")
 #cursor.executemany(query, values)
 #db.commit()
 #print("GOT THIS FAR2")
 #cursor.execute("SELECT coffeeid, temperature, time from cofset;")
 #records = cursor.fetchall()
 #print(records)
 #return timer(req)
  
  
#def coffeeset(req):
  # View the Dictionary that was Posted
  # Get the fname
  #print("bbbeeeeeppppp")
  #temp = str(req.params.getall("temperature"))
  #date = str(req.params.getall("date"))
  #time = str(req.params.getall("time"))
  #recur = str(req.params.getall("recur"))
  # Get rid of the [] that comes from req
  #temp = temp[2:len(temp)-2]
  #date = date[2:len(date)-2]
  #time = time[2:len(time)-2]
  #recur = recur[2:len(recur)-2]
  #msg ='{"temperature": "'+temp+'", "date": "' +date+ '", "time": "'+time+'", "recur": "'+recur+'"}'
  #print(msg)
  # SEND TO RASPBERRY PI WITH MQTT
  #client = mqtt.Client("JJJ")
  #client.connect("polarcoffee.org", port=1883, keepalive=60, bind_address="")
  #client.publish("test", msg)
  #records = {}
  #records['success'] = True
  #records = Response(body=json.dumps(records))
  #records.headers.update({'Access-Control-Allow-Origin': '*',})

  #return records
  #SEND TO DATABASE
  #db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  #cursor = db.cursor()
  # Insert Records
  #query = "insert into cofset (coffeeid, temperature, time) values (%s, %s, %s)"
  #values = [
  #("testid", temp, time),
  #]
  #print("GOT THIS FAR1")
  #cursor.executemany(query, values)
 # db.commit()
 # print("GOT THIS FAR2")
  #cursor.execute("SELECT coffeeid, temperature, time from cofset;")
  #records = cursor.fetchall()
  #print(records)


def setcoffee(req):
  if 'user' in req.session: # logged in
    return render_to_response('templates/setter.html',{'user':req.session['user']})
  else: # not logged in
    return HTTPFound(req.route_url("login"))
  
  
  #return render_to_response('templates/setter.html', {'username': req.params['username']}, request =req)
  
def setter(req):
  if 'user' in req.session: # logged in
    return render_to_response('templates/setter.html',{'user':req.session['user']})
  else: # not logged in
    return HTTPFound(req.route_url("login"))
  
  





############################################

def get_members(req):
  # Connect to the database and retrieve the users
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select count(id) from Users;")
  records = cursor.fetchall()
  db.close()
  value_to_return = {}
  value_to_return['records'] = records[0]
  value_to_return = Response(body=json.dumps(value_to_return))
  #records = records[1:len(records)-1]
  print(records)
  return value_to_return

############################################


def get_visit(req):
  # Connect to the database and retrieve the visit info
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select count(id) from visits where route_name = 'Home' and session_id = 'No user logged in.'")
  anonymousHome = cursor.fetchall()
  cursor.execute("select count(id) from visits where route_name = 'Home' and session_id != 'No user logged in.'")
  loggedHome = cursor.fetchall()
  cursor.execute("select count(id) from visits where route_name = 'About' and session_id = 'No user logged in.'")
  anonymousAbout = cursor.fetchall()
  cursor.execute("select count(id) from visits where route_name = 'About' and session_id != 'No user logged in.'")
  loggedAbout = cursor.fetchall()
  cursor.execute("select count(id) from visits where route_name = 'Features' and session_id = 'No user logged in.'")
  anonymousFeatures = cursor.fetchall()
  cursor.execute("select count(id) from visits where route_name = 'Features' and session_id != 'No user logged in.'")
  loggedFeatures = cursor.fetchall()
  cursor.execute("select count(id) from visits where route_name = 'Pricing' and session_id = 'No user logged in.'")
  anonymousPricing = cursor.fetchall()
  cursor.execute("select count(id) from visits where route_name = 'Pricing' and session_id != 'No user logged in.'")
  loggedPricing = cursor.fetchall()
  cursor.execute("select count(id) from visits where route_name = 'Sign Up' and session_id = 'No user logged in.'")
  anonymousSignUp = cursor.fetchall()
  cursor.execute("select count(id) from visits where route_name = 'Sign Up' and session_id != 'No user logged in.'")
  loggedSignUp = cursor.fetchall()
  cursor.execute("select count(id) from visits where route_name = 'Metrics' and session_id = 'No user logged in.'")
  anonymousMetrics = cursor.fetchall()
  cursor.execute("select count(id) from visits where route_name = 'Metrics' and session_id != 'No user logged in.'")
  loggedMetrics = cursor.fetchall()
  db.close()
  
  value_to_return = {}
  value_to_return['records'] = anonymousHome + loggedHome + anonymousAbout + loggedAbout + anonymousFeatures + loggedFeatures + anonymousPricing + loggedPricing + anonymousSignUp + loggedSignUp + anonymousMetrics + loggedMetrics
  value_to_return = Response(body=json.dumps(value_to_return))
  #records = records[1:len(records)-1]
  print(value_to_return)
  return value_to_return


















############################################

def get_news(req):
  # Connect to the database and retrieve the news
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select * from newsupdates;")
  record = cursor.fetchall()
  db.close()
  value_to_return = {}
  value_to_return['record'] = record
  value_to_return = Response(body=json.dumps(value_to_return))
  #record = record[1:len(record)-1]
  print(record)
  return value_to_return

############################################

def portal(req):
  start = time.time()
  session_id = {}
  if 'user' in req.session: # logged in
    # Connect to the database
    session_id = req.session['user']
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    # Insert Records
    query = "insert into visits (session_id, route_name, timestamp) values (%s, %s, %s)"
    values = [
    (session_id,'Home',start),
    ]
    cursor.executemany(query, values)
    db.commit() 
    return render_to_response('templates/portal.html',{'user':req.session['user']})
  else: # not logged in
    # Connect to the database
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    # Insert Records
    query = "insert into visits (session_id, route_name, timestamp) values (%s, %s, %s)"
    values = [
    ('No user logged in.','Home',start),
    ]
    cursor.executemany(query, values)
    db.commit()
    return render_to_response('templates/portal.html', {}, request =req)

############################################


def get_ready(req):
  # Connect to the database and retrieve the news
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select days from ready where id=1;")
  recorded = cursor.fetchall()
  db.close()
  value_to_return = {}
  value_to_return['recorded'] = recorded
  value_to_return = Response(body=json.dumps(value_to_return))
  #record = record[1:len(record)-1]
  print(recorded)
  return value_to_return







def add_new_user(req):
  # Get all the data that is going to be sent (needs to be a dict like "data")
  # print(req.params) #debugging
  data = {"Email": req.params['Email'], "Password":  req.params['Password']}
  #New_user = requests.post(REST_SERVER + '/new_users', data=data).json()
  New_user = requests.post('https://polarcoffee.org:6001/new_users', data=data).json()
  return render_to_response('templates/portal.html', {}, request=req)

def add_users_db(req):
  # View the Dictionary that was Posted
  # Get the Password
  newPsw = str(req.params.getall("Password"))
  # Get rid of the [] that comes from req
  newPsw = newPsw[2:len(newPsw)-2]
  # Get the name the user entered
  newName = str(req.params.getall("Email"))
  # Get rid of the [] that comes from req
  newName = newName[2:len(newName)-2]
  # Connect to the database
  db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  cursor = db.cursor()
  # Insert Records
  query = "insert into Users (Email, Password, Status) values (%s, %s, %s)"
  values = [
  (newName,newPsw,'Pending'),
  ]
  cursor.executemany(query, values)
  db.commit()
  cursor.execute("SELECT Email, Password, Status from Users;")
  records = cursor.fetchall()
  json.dumps(records) #take this out?
  return render_to_response('templates/portal.html', {}, request =req)

# Compare credentials from request (from user) to json
def correct_password(req):
  data = {"Email": req.params['Email'], "Password":  req.params['Password']}
  #validity = requests.post(REST_SERVER + '/check_password', data = data).json()
  validity = requests.post('https://polarcoffee.org:6001/check_password', data = data).json()
  return validity

def valid_user(req):
  try:
    data = {"Email": req.params['Email']}
  except:
    data = req
  #validity = requests.post(REST_SERVER + '/check_validity', data = data).json()
  validity = requests.post('https://polarcoffee.org:6001/check_validity', data = data).json()
  return validity

# These currently just render the html files 
def sign_up(req):
  start = time.time()
  session_id = {}
  if 'user' in req.session: # logged in
    # Connect to the database
    session_id = req.session['user']
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    # Insert Records
    query = "insert into visits (session_id, route_name, timestamp) values (%s, %s, %s)"
    values = [
    (session_id,'Sign Up',start),
    ]
    cursor.executemany(query, values)
    db.commit() 
    return render_to_response('templates/sign_up.html',{'user':req.session['user']})
  else: # not logged in
    # Connect to the database
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    # Insert Records
    query = "insert into visits (session_id, route_name, timestamp) values (%s, %s, %s)"
    values = [
    ('No user logged in.','Sign Up',start),
    ]
    cursor.executemany(query, values)
    db.commit()
    return render_to_response('templates/sign_up.html', {}, request =req)










def about(req):
  start = time.time()
  session_id = {}
  if 'user' in req.session: # logged in
    # Connect to the database
    session_id = req.session['user']
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    # Insert Records
    query = "insert into visits (session_id, route_name, timestamp) values (%s, %s, %s)"
    values = [
    (session_id,'About',start),
    ]
    cursor.executemany(query, values)
    db.commit() 
    return render_to_response('templates/about.html',{'user':req.session['user']})
  else: # not logged in
    # Connect to the database
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    # Insert Records
    query = "insert into visits (session_id, route_name, timestamp) values (%s, %s, %s)"
    values = [
    ('No user logged in.','About',start),
    ]
    cursor.executemany(query, values)
    db.commit()
    return render_to_response('templates/about.html', {}, request =req)
  
  
  
  
  
  
  
  
  
  
  
  
  

def pricing(req):
  start = time.time()
  session_id = {}
  if 'user' in req.session: # logged in
    # Connect to the database
    session_id = req.session['user']
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    # Insert Records
    query = "insert into visits (session_id, route_name, timestamp) values (%s, %s, %s)"
    values = [
    (session_id,'Pricing',start),
    ]
    cursor.executemany(query, values)
    db.commit() 
    return render_to_response('templates/pricing.html',{'user':req.session['user']})
  else: # not logged in
    # Connect to the database
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    # Insert Records
    query = "insert into visits (session_id, route_name, timestamp) values (%s, %s, %s)"
    values = [
    ('No user logged in.','Pricing',start),
    ]
    cursor.executemany(query, values)
    db.commit()
    return render_to_response('templates/pricing.html', {}, request =req)

def features(req):
  start = time.time()
  session_id = {}
  if 'user' in req.session: # logged in
    # Connect to the database
    session_id = req.session['user']
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    # Insert Records
    query = "insert into visits (session_id, route_name, timestamp) values (%s, %s, %s)"
    values = [
    (session_id,'Features',start),
    ]
    cursor.executemany(query, values)
    db.commit() 
    return render_to_response('templates/features.html',{'user':req.session['user']})
  else: # not logged in
    # Connect to the database
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    # Insert Records
    query = "insert into visits (session_id, route_name, timestamp) values (%s, %s, %s)"
    values = [
    ('No user logged in.','Features',start),
    ]
    cursor.executemany(query, values)
    db.commit()
    return render_to_response('templates/features.html', {}, request =req)

def metrics(req):
  start = time.time()
  session_id = {}
  if 'user' in req.session: # logged in
    # Connect to the database
    session_id = req.session['user']
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    # Insert Records
    query = "insert into visits (session_id, route_name, timestamp) values (%s, %s, %s)"
    values = [
    (session_id,'Metrics',start),
    ]
    cursor.executemany(query, values)
    db.commit() 
    return render_to_response('templates/metrics.html',{'user':req.session['user']})
  else: # not logged in
    # Connect to the database
    db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    cursor = db.cursor()
    # Insert Records
    query = "insert into visits (session_id, route_name, timestamp) values (%s, %s, %s)"
    values = [
    ('No user logged in.','Metrics',start),
    ]
    cursor.executemany(query, values)
    db.commit()
    return render_to_response('templates/metrics.html', {}, request =req)

def visitor_analytics(req):
  if 'user' in req.session: # logged in
    return render_to_response('templates/visitor_analytics.html',{'user':req.session['user']})
  else: # not logged in
    return HTTPFound(req.route_url("login"))











def timer(req):
  return render_to_response('templates/timer.html', {}, request =req)



''' Route Configurations '''
if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route('v2', '/')
  # Loading stuff from the server
  config.add_view(portal, route_name='v2') #change to controller


  config.add_route('new_user', '/new_user')
  #For view users(quick debugging)
  #config.add_view(show_users, route_name='new_user')
  # What send info over to the Rest Server
  config.add_view(add_new_user, route_name='new_user', request_method = "POST")

  config.add_route('sign_up', '/sign_up')
  config.add_view(sign_up, route_name='sign_up')
  
   ##########ADDED
  config.add_route('add_new_user', '/new_users')
  config.add_view(add_users_db, route_name='add_new_user', renderer='json')
  

  
  
  
  
  
  config.add_route('login', '/login')
  config.add_view(login, route_name='login')

  config.add_route('get_home', '/home')
  config.add_view(get_home, route_name='get_home')
  
  config.add_route('visitor_analytics', '/admin') # Added route for analytics rendering
  config.add_view(visitor_analytics, route_name='visitor_analytics')
 
  config.add_route('post_login', '/post_login')
  config.add_view(post_login, route_name='post_login', request_method = "POST")

  config.add_route('about', '/about') # Added route for about
  config.add_view(about, route_name='about')
  
  config.add_route('features', '/features') # Added route for features
  config.add_view(features, route_name='features')
  
  config.add_route('pricing', '/pricing') # Added route for pricing
  config.add_view(pricing, route_name='pricing')
  
  config.add_route('metrics', '/metrics') # Added route for metrics rendering
  config.add_view(metrics, route_name='metrics')
    
  config.add_route('setter', '/setter') # Added route for setter
  config.add_view(setter, route_name='setter')
  
  config.add_route('timer', '/timer') # Added route for timer
  config.add_view(timer, route_name='timer')
  
  config.add_route('coffeeset', '/coffeeset') # Added route for timer
  config.add_view(coffeeset, route_name='coffeeset')
  
  
  
  ##################################
  
  config.add_route('get_members', '/get_members')
  config.add_view(get_members, route_name='get_members', renderer='json')
  
  ##################################
  
  ##################################
  
  config.add_route('get_news', '/get_news')
  config.add_view(get_news, route_name='get_news', renderer='json')
  
  ##################################
  
  
  config.add_route('get_visit', '/get_visit')
  config.add_view(get_visit, route_name='get_visit', renderer='json')
  
  ##################################
  
  config.add_route('get_ready', '/get_ready')
  config.add_view(get_ready, route_name='get_ready', renderer='json')
  
  ##################################
  
  config.add_route('spotify', '/spotify')
  config.add_view(spotify, route_name='spotify', renderer='json')
  
  config.add_route('get_playlists', '/get_playlists')
  config.add_view(get_playlists, route_name='get_playlists', renderer='json')



  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  
    # Create the session using a signed
  session_factory = SignedCookieSessionFactory(os.environ['SESSION_SECRET_KEY'])
  config.set_session_factory(session_factory)
  
  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()
