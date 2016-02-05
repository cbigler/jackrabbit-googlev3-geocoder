import geopy

from rate_limiter import RateLimiter


class Geocoder(object):
    def __init__(self, api_key=None, client_id=None, secret_key=None):
        if api_key:
            self._geolocator = geopy.GoogleV3(api_key=api_key)
        elif client_id and secret_key:
            self._geolocator = geopy.GoogleV3(client_id=client_id, secret_key=secret_key)
        else:
            raise ValueError('One of either the api_key or both client_id and secret_key must be provided.')

        self._geocode_limiter = RateLimiter(10)
        self._reverse_limiter = RateLimiter(10)

    def geocode(self, address):
        self._geocode_limiter.wait()
        loc = self._geolocator.geocode(address)
        return [loc.latitude, loc.longitude]

    def reverse(self, latitude, longitude):
        self._reverse_limiter.wait()
        loc = self._geolocator.reverse((latitude, longitude), exactly_one=True)
        return loc.address
