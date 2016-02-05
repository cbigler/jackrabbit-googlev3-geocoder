from src.proxy import GeocoderProxy


def print_response(response):
    if resp:
        print('Success: {}'.format(resp.return_value))
    else:
        print('Error: ({}) {}'.format(resp.code, resp.details))


proxy = GeocoderProxy('amqp://dev:dev@localhost/geocoder')

resp = proxy.geocode('1600 Amphitheatre Parkway, Mountain View, CA 94043')
print_response(resp)

resp = proxy.reverse(latitude=42, longitude=-75)
print_response(resp)
