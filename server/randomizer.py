import socket
import threading
import pathlib
import random
from pathlib import Path
from GPIO import LED
import time
from models import Recording

class Randomizer:

	def __init__(self, directory, r_port, s_port, db_session=None):
		self.directory = directory
		self.receive_port = r_port
		self.send_port = s_port
		self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)       		
		self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.receive_socket.bind(('localhost', self.receive_port))
		self.current_track = 0
		self.project_name = None
		self.recording_track_path = None
		self.led = LED()
		self.led_thread = threading.Thread(target=self.toggle_led, daemon=True)
		self.led_toggling = False
		self.led_thread.start()
		self.db_session = db_session

	def send(self, msg):
		self.send_socket.sendto(msg.encode(), ('localhost', self.send_port))

	def toggle_led(self):
		while(1):
			if(self.led_toggling == True):
				self.led.on()
				time.sleep(0.5)
				self.led.off()
				time.sleep(0.5)
			else:
				time.sleep(0.2)

	def parse_message(self, msg):
		if msg == 'get_random_file;':
			self.get_random_file()
		if msg == 'get_next_file;':
			self.get_next_file()
		if msg == 'recording_start;':
			self.led.on()
		if msg == 'recording_ending;':
			self.led_toggling = True
		if msg == 'recording_end;':
			print(f'recording end - {self.current_track}')
			self.led_toggling = False
			self.led.off()
			if (db_session != None):
				self.save_file_data()
		if 'rFile' in msg:
			tokens = msg.split(':')
			self.recording_track_path = tokens[1].strip(';')
			print(self.recording_track_path)

	def get_next_file(self):
		path = Path(self.directory)
		files = list(path.iterdir())
		next_file = str(files[self.current_track])
		self.send(f'loopFile {next_file};\n')
		self.current_track = (self.current_track + 1) % len(files)

	def get_random_file(self):
		path = Path(self.directory)
		files = list(path.iterdir())
		num_files = len(files)
		random_file = files[random.randint(0, num_files - 1)]
		print(random_file)
		self.send(f'loopFile {str(random_file)};\n')

	def set_project_name(self, n):
		print('Setting project name to {n}')
		self.current_project_name = n

	def save_file_data(self):
		file_name = self.recording_track_path.split('/')[-1]
		#r = Recording(self.)

	def run(self):
		while 1:
			data = self.receive_socket.recv(1024)
			print(data)
			self.parse_message(data.decode().strip())

	def start(self):
		t1 = threading.Thread(target=self.run)
		t1.start()

