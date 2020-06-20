from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import Response
from spotipy import Spotify
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
from bottle import route, run, request

from pyramid.httpexceptions import HTTPFound            # Perform redirects from the backend to other routes
# NOTE: this is unencrypted but signed session stored in client cookies. It isn't the most secure, but at least it's baked into Pyramid. Shame on Pyramid!
from pyramid.session import SignedCookieSessionFactory  # The default session factory to generate session objects

import mysql.connector as mysql
import requests
import json
import os
import time
import paho.mqtt.client as mqtt
import sys
import spotipy
import spotipy.util as util


db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

SPOTIPY_CLIENT_ID = '531bf1de1dc44e71bd4bb4f9c69af7a7'
SPOTIPY_CLIENT_SECRET = '0d6921a912534d15b5fed7e75b4f46b2'
SPOTIPY_REDIRECT_URI = 'http://polarcoffee.org/spotify'
SCOPE = 'playlist-modify-public'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

def spotify(req):
  return render_to_response('templates/spotify.html', {}, request =req)

@route('/')
def get_playlists(req):
        
    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return results

    else:
        return htmlForLoginButton()

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url


''' Route Configurations '''
if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')
  
  config.add_route('spotify', '/spotify')
  config.add_view(spotify, route_name='spotify', renderer='json')
  
  config.add_route('get_playlists', '/get_playlists')
  config.add_view(get_playlists, route_name='get_playlists', renderer='json')
  
  #######not sure if these are needed
  
  #config.add_route('getSPOauthURI', '/getSPOauthURI')
  #config.add_view(getSPOauthURI, route_name='getSPOauthURI', renderer='json')
  
  #config.add_route('htmlForLoginButton', '/htmlForLoginButton')
  #config.add_view(htmlForLoginButton, route_name='htmlForLoginButton', renderer='json')


  config.add_static_view(name='/', path='./public', cache_max_age=3600)
  
    # Create the session using a signed
  session_factory = SignedCookieSessionFactory(os.environ['SESSION_SECRET_KEY'])
  config.set_session_factory(session_factory)
  
  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()
