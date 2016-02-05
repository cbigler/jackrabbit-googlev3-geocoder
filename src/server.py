import jackrabbit
import logging
import sys

from impl.geocoder import Geocoder

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

API_KEY = 'YOUR_API_KEY'
geocoder = Geocoder(api_key=API_KEY)

server = jackrabbit.Server('amqp://dev:dev@localhost/geocoder')
server.register_handler('geocode', 1, geocoder.geocode)
server.register_handler('reverse', 1, geocoder.reverse)
server.run()
