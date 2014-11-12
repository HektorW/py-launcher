
import http.server
import time

IP = ''
PORT = 8000


class LauncherRequestHandler(http.server.BaseHTTPRequestHandler):

	def do_GET(self): 
		print('GET')
		print('---', self.client_address)
		print('---', self.path)
		self.send_response(200)
		self.send_header("Content-Type", "text/plain")
		self.end_headers()
		self.sendString("Hello world")


	def sendString(self, str):
		self.wfile.write(bytes(str, "UTF-8"))




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