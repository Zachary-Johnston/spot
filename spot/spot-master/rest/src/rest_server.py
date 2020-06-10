from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.renderers import render_to_response

import json
import mysql.connector as mysql
import os
import requests
import time
import paho.mqtt.client as mqtt


                ##############################################################################
                #                 Including completed code from assignment API
                ##############################################################################
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']


def coffeeset(req):
  # View the Dictionary that was Posted
  # Get the fname
  print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
  info = req.json_body
  print(info)

  msg = json.dumps(info)
  print(msg)
  # SEND TO RASPBERRY PI WITH MQTT
  client = mqtt.Client("JJJ")
  client.connect("polarcoffee.org", port=1883, keepalive=60, bind_address="")
  client.publish("test", msg)
  
  records = {}
  records['success'] = True
  records = Response(body=json.dumps(records))
  records.headers.update({'Access-Control-Allow-Origin': '*',})

  return records

if __name__ == '__main__':
  config = Configurator()

  config.add_route('coffeeset', '/coffeeset') # Added route for timer
  config.add_view(coffeeset, route_name='coffeeset')
  

              ##############################################################################
              #                        Adding Routes to Database                           #
              ##############################################################################



              ##############################################################################
              #                        --END OF CODE ---                                   #
              ##############################################################################
  

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()
