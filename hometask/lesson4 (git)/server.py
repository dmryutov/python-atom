# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server

from tasks import Roadmap


class SimpleWSGIApplication:
	def __init__(self, environment, start_response):
		self.environment = environment
		self.start_response = start_response
		self.headers = [('Content-type', 'text/plain; charset=utf-8')]
		self.roadmap = Roadmap()
		self.roadmap.loadTasks()

	def __iter__(self):
		if self.environment.get('PATH_INFO', '/') == '/':
			yield from self.ok_response()
		else:
			self.not_found_response()

	def not_found_response(self):
		self.start_response('404 Not Found', self.headers)

	def ok_response(self):
		message = ''
		for t in self.roadmap.critical:
			message += str(t)
		status = '204 No Content' if message == '' else '200 OK'

		self.start_response(status, self.headers)
		yield (message.encode('utf8'))


server = make_server('127.0.0.1', 8080, SimpleWSGIApplication)
server.serve_forever()