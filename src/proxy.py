import jackrabbit


class GeocoderProxy(jackrabbit.ProxyBase):
    def __init__(self, uri):
        super(GeocoderProxy, self).__init__(uri)

    def geocode(self, address):
        return self.exec_rpc('geocode', 1, address=address)

    def reverse(self, latitude, longitude):
        return self.exec_rpc('reverse', 1, latitude=latitude, longitude=longitude)

