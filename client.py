
import http.client
import threading
import multiprocessing
import sys


IP_PATTERN = '157.125.54.*'
SERVER_PORT = 7202

lock = threading.Lock()
ips = []
thread_count = 0
callback_count = 0

def callback(ip, is_server):
	done = False
	with lock:
		global callback_count
		global thread_count
		callback_count += 1
		if is_server:
			ips.append(ip)
		if callback_count == thread_count:
			done = True
	if done:
		sweep_done(ips)
			

def sweep_done(connected_ips):
	print('sweep done, connection to', connected_ips)
	for ip in connected_ips:
		launch_remote(ip, SERVER_PORT)

def launch_remote(ip, port):
	conn = http.client.HTTPConnection(ip, port)
	conn.request('GET', '/launch/starcraft')
	response = conn.getresponse()
	print(response.status, response.reason, response.read().decode('utf-8'))

def can_connect(ip, port, callback):
	try:
		conn = http.client.HTTPConnection(ip, port, timeout=2)
		conn.request('GET', '/ping')
		response = conn.getresponse()
		if response.status == 200 and response.reason == 'OK':
			content = response.read().decode('utf-8')
			if content == 'pong':
				sys.stdout.write(ip + ' is a server\n')
				callback(ip, True)
			else:
				sys.stdout.write(ip + ' is a server but is not responding correctly\n')
				callback(ip, False)
	except:
		sys.stdout.write(ip + ' is not a server\n')
		callback(ip, False)
	

def scan_network(ip_pattern, port, connected_ips=[]):
	"""
	Pattern where '*' will be replaced with {0-255}
	"""
	if ip_pattern.find('*') is not -1:
		for i in range(0, 255):
			ip = ip_pattern.replace('*', str(i), 1)
			scan_network(ip, port, connected_ips)
	else:
		t = threading.Thread(target=can_connect, args=(ip_pattern, port, callback))
		t.start()
		global thread_count
		thread_count += 1
		# alive = can_connect(ip_pattern, port)
		# if alive:
			# connected_ips.append(ip_pattern)
			# print(ip_pattern, 'is connected')
	# return connected_ips


# print(scan_network(IP_PATTERN, SERVER_PORT))
# print(multiprocessing.cpu_count())
scan_network(IP_PATTERN, SERVER_PORT)