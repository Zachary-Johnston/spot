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







''' Route Configurations '''
if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')
  
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
