
import string
import json
import os
import time

from ctypes import windll
from subprocess import call


class Launcher:
	"""
	Class which scans file system for Starcraft 2 and can launch it.
	Stores scan data between sessions.
	"""

	SCAN_FILE = 'scan.json'

	DIR_LEADS = [
		'program files',
		'program files (x86)',
		'games',
		'starcraft 2',
		'starcraft ii',
		'battle.net',
		'programs',
		'program',
		'spel'
	]

	FILE_NAMES = [
		'starcraft ii.exe',
		'starcraft 2.exe',
		'starcraft2.exe',
		'sc ii.exe',
		'sc 2.exe',
		'sc2.exe'
	]

	def __init__(self):
		self.data = self.read_scan_file(self.SCAN_FILE)
		if not 'starcraft' in self.data:
			start_time = time.time()
			self.data['lastscan'] = start_time
			starcraft_path = self.scan_all(self.FILE_NAMES, self.DIR_LEADS)
			if starcraft_path is not None:
				self.data['starcraft'] = starcraft_path
				self.write_scan_file(self.SCAN_FILE)
			else:
				print('No starcarft path found')
		print('data', self.data)


	def write_scan_file(self, filename):
		"""
		Wrítes data to file
		"""
		with open(filename, 'w') as f:
			f.write(json.dumps(self.data))


	def read_scan_file(self, filename):
		"""
		Check for any stored data from earlier sessions
		"""
		if not os.path.isfile(filename):
			return {}
		with open(filename, 'r') as f:
			try:
				return json.load(f)
			except e: #ValueError
				print("Invalid JSON: ", e)
				pass


	def start_process(self, name):
		"""
		Start a sub process from data by name
		"""
		if name in self.data:
			call(self.data[name])
			return True
		return False


	def get_drives(self):
		"""
		Get possible drives from local filesystem
		"""
		DRIVE_FIXED = 3
		drives = []
		for letter in string.ascii_uppercase:
			drive = '%s:\\' % letter
			if windll.kernel32.GetDriveTypeW(drive) is DRIVE_FIXED:
				drives.append(drive)
		return drives


	def scan_all(self, search, leads=None):
		"""
		Scan entire filesystem for searched files.
		If leads is not None, exclude directories not in leads.
		"""
		drives = self.get_drives()
		for drive in drives:
			for dirpath, dirnames, filenames in os.walk(drive, topdown=True):
				for f in filenames:
					if f.lower() in search:
						return os.path.join(dirpath, f)
				# Excludes 
				if leads is not None:
					dirnames[:] = [d for d in dirnames if d.lower() in leads]
		return None
				
