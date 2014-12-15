
from launcher import Launcher
from routes import Mapper
from collections import defaultdict

import http.server
import time


IP = ''
PORT = 7202


launcher = Launcher()

router = Mapper()
router.connect('/ping', controller='connection', action='ping')
router.connect('/launch/{game}', controller='launcher', action='launch')


def launch(request, response):
	game = request['game']
	if game is not None:
		result = launcher.start_process(game)
		if result:
			response.writeString('game launched: ' + game)
		else:
			response.writeString('could not launch game: ' + game)
	else:
		response.writeString('no game supplied')


controllers = defaultdict(lambda: None, {
	'connection': {
		'ping': {
			'status': 200,
			'msg': 'pong'
		}
	},
	'launcher': {
		'launch': {
			'status': 200,
			'task': launch
		}
	}
})


class LauncherRequestHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self): 
		handleRequest(self, self.path)

	def writeString(self, str):
		self.wfile.write(bytes(str, "UTF-8"))


def handleRequest(response, path):
	request = router.match(path)

	if request is None or 'controller' not in request:
		print('no controller for request', request)
		response.send_response(400)
		response.end_headers()
		return

	controller = controllers[request['controller']]
	if controller is not None:

		if request['action'] in controller:
			action = controller[request['action']]

			# Headers
			response.send_response(action['status'])
			response.send_header('Content-Type', 'text/plain')
			response.end_headers()

			if 'task' in action:
				task = action['task']
				result = task(request, response)

			if 'msg' in action:
				response.writeString(action['msg'])

		else:
			response.send_response(500)
			response.end_headers()
			print('no valid action for ', request['action'])
	else:
		response.send_response(500)
		response.end_headers()
		print('no valid controller for ', request['controller'])
	


def run(server=http.server.HTTPServer, handler=http.server.BaseHTTPRequestHandler):
	address = (IP, PORT)
	httpd = server(address, handler)
	print(time.asctime(), "Server starts - %s:%s" % address)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print(time.asctime(), "Server stops - %s:%s" % address)



if __name__ == '__main__':
	run(http.server.HTTPServer, LauncherRequestHandler)


# not related to anything else, but whatevs
def fuzzySearch(strings, query):
	matches = [string for string in strings if re.search(".*?".join(query), strings)]
	return matches
