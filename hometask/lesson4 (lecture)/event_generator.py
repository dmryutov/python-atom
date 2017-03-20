from random import randint
from time import sleep
from wsgiref.simple_server import make_server


def events(max_delay, limit):
    while True:
        delay = randint(1, max_delay)
        if delay >= limit:
            sleep(limit)
            yield None
        else:
            sleep(delay)
            yield 'Event generated, awaiting %ds' % delay

generator = events(10, 5)

class SimpleWSGIApplication:
    def __init__(self, environment, start_response):
        print('\nGet request')
        self.environment = environment
        self.start_response = start_response
        self.headers = [('Content-type', 'text/plain; charset=utf-8')]

    def __iter__(self):
        print('Wait for response')
        if self.environment.get('PATH_INFO', '/') == '/':
            yield from self.ok_response(generator)
        else:
            self.not_found_response()
        print('Done')

    def not_found_response(self):
        print('Create response')
        print('Send headers')
        self.start_response('404 Not Found', self.headers)
        print('Headers is sent')

    def ok_response(self, response):
        print('Create response')
        print('Send headers')
        message = next(response)
        if message == None:
            status  = '204 No Content'
        else:
            status = '200 OK'
        self.start_response(status, self.headers)
        print('Headers is sent')
        yield ('%s\n' % message).encode('utf-8')
        print('Body is sent')


server = make_server('127.0.0.1', 8080, SimpleWSGIApplication)
server.serve_forever()