from Geohash import geohash
import geopy

from rate_limiter import RateLimiter


class Geocoder(object):
    def __init__(self, api_key=None, client_id=None, secret_key=None, reverse_cache_geohash=9):
        if api_key:
            self._geolocator = geopy.GoogleV3(api_key=api_key)
        elif client_id and secret_key:
            self._geolocator = geopy.GoogleV3(client_id=client_id, secret_key=secret_key)
        else:
            raise ValueError('One of either the api_key or both client_id and secret_key must be provided.')

        self._geocode_limiter = RateLimiter(10)
        self._reverse_limiter = RateLimiter(10)

        self._reverse_cache_geohash_length = reverse_cache_geohash
        self._reverse_cache = {}

    def _using_cache(self):
        return 0 < self._reverse_cache_geohash_length <= 12

    def geocode(self, address):
        self._geocode_limiter.wait()
        loc = self._geolocator.geocode(address)
        return [loc.latitude, loc.longitude]

    def reverse(self, latitude, longitude):
        addr = None

        # try to get the address from the local cache, if we're using it
        if self._using_cache():
            ghash = geohash.encode(float(latitude), float(longitude), self._reverse_cache_geohash_length)
            addr = self._reverse_cache.get(ghash)

        # if we didn't get the address from the cache, or we're not using the cache
        # then get it from Google
        if not addr:
            self._reverse_limiter.wait()
            loc = self._geolocator.reverse((latitude, longitude), exactly_one=True)
            addr = loc.address

        # if we're using the cache, save the value we just got back
        if addr and self._using_cache():
            self._reverse_cache[ghash] = addr

        return addr
