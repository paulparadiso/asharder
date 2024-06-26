import socket
import threading
import pathlib
import random
from pathlib import Path
from GPIO import LED, Button
import time
from database import db_session
from models import Recording
from datetime import datetime
import s3manager

DEFAULT_PROJECT_NAME = 'UNSORTED'

class Randomizer:

	def __init__(self, directory, r_port, s_port, db_session=None):
		self.directory = directory
		self.receive_port = r_port
		self.send_port = s_port
		self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)       		
		self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.receive_socket.bind(('localhost', self.receive_port))
		self.current_track = 0
		self.project_name = DEFAULT_PROJECT_NAME
		self.recording_track_path = None
		self.last_command = None
		self.play_mode = 'loop'
		self.button = None
		self.current_shuffle_file = None
		self.led = LED()
		self.led_thread = threading.Thread(target=self.toggle_led, daemon=True)
		self.led_toggling = False
		self.led_thread.start()
		self.db_session = db_session
		self.last_command = ''

	def send(self, msg):
		print(msg)
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
		print(msg)
		#if msg == 'get_random_file;':
		#	self.get_random_file()
		#if msg == 'get_next_file;':
		#	self.get_next_file()
		#if msg == 'recording_start;':
		#	self.led.on()
		#if msg == 'recording_ending;':
		#	self.led_toggling = True
		#if msg == 'recording_end;':
		#	print(f'recording end - {self.current_track}')
		#	self.led_toggling = False
		#	self.led.off()
		#	self.save_file_data()
		#if 'rFile' in msg:
		#	tokens = msg.split(':')
		#	self.recording_track_path = tokens[1].strip(';')
		#	print(self.recording_track_path)
		if msg == 'led_on;':
			self.led.on()
		elif msg == 'led_off;':
			self.led.off()
		elif msg == 'recording_done;':
			self.save_file_data()

	def get_tempo(self, file):
		r = 0
		try:
			r = file.split('.')[0].split('_')[1]
		except:
			pass
		return r

	def get_next_file(self):
		path = Path(self.directory)
		files = list(path.iterdir())
		if len(files) < 1:
			return
		self.current_shuffle_file = str(files[self.current_track])
		#tempo = self.get_tempo(next_file)
		self.send(f'loopFile {self.current_shuffle_file};\n')
		#self.send(f'tempo {str(tempo)};\n')
		self.current_track = (self.current_track + 1) % len(files)
		self.last_command = 'shuffle:play'
		
	def send_last_file(self):
		if self.current_shuffle_file != None:
			self.send(f'loopFile {self.current_shuffle_file};\n')

	def get_random_file(self):
		path = Path(self.directory)
		files = list(path.iterdir())
		num_files = len(files)
		random_file = files[random.randint(0, num_files - 1)]
		tempo = self.get_tempo(random_file)
		print(random_file)
		self.send(f'loopFile {str(random_file)};\n')
		self.send(f'tempo {str(tempo)};\n')

	def set_project_name(self, n):
		print('Setting project name to {n}')
		self.project_name = n

	def set_record_time(self, t):
		self.record_time = int(t)
		self.send(f'recordTime {self.record_time};\n')

	def save_file_data(self):
		print('Saving file data.')
		file_name = self.recording_track_path.split('/')[-1]
		r = Recording(self.project_name, file_name, self.recording_track_path)
		db_session.add(r)
		db_session.commit()

	def start_recording(self):
		if self.last_command != 'record:start':
			recording_file = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.wav'
			self.recording_track_path = f'/home/pi/recordings/{recording_file}'
			print(self.recording_track_path)
			self.send('command stopLoop;\n')
			self.send(f'recordFile {self.recording_track_path};\n')
			self.last_command = 'record:start'
		else:
			self.send(f'command stopRecording;\n')
			self.save_file_data()
			self.last_command = 'record:stop'

	def play_or_stop_file(self):
		if self.last_command == None:
			return
		elif self.last_command == 'shuffle:play':
			self.send('command stopLoop;\n')
			self.last_command = 'shuffle:stop'
		elif self.last_command == 'shuffle:stop':
			self.send_last_file()
			self.last_command = 'shuffle:play'
		elif self.last_command == 'record:stop' or self.last_command == 'play:stop':
			self.play_last_recording()
			self.last_command = 'play:start'
		elif self.last_command == 'play:start':
			self.send('command stopLoop;\n')
			self.last_command = 'play:stop'
		elif self.last_command == 'record:start':
			self.send(f'command stopRecording;\n')
			self.last_command = 'record:stop'
			self.play_or_stop_file()

	def save_current_file(self):
		if self.recording_track_path != None:
			#self.save_file_data()
			r = db_session.query(Recording).filter(Recording.path == self.recording_track_path).first()
			r.upload = True
			db_session.commit()

	#def save_file_data(self):
	#	r = db_session.query(Recording).filter(Recording.path == self.recording_track_path).first()
	#	r.upload = True
	#	db_session.commit()

	def send_current_file(self):
		if self.recording_track_path == None:
			return
		if db_session.query(Recording).filter(Recording.path == self.recording_track_path).first() is None:
			self.save_file_data()
		r = db_session.query(Recording).filter(Recording.path == self.recording_track_path).first()
		r.upload = True
		db_session.commit()
		s3manager.upload_files()

	def erase_current_file(self):
		if(self.recording_track_path == None):
			return
		db_session.query(Recording).filter(Recording.path == self.recording_track_path).delete()
		db_session.commit()
		file = pathlib.Path(self.recording_track_path)
		if(file.is_file()):
			file.unlink()
		self.recording_track_path = None
		
	def play_last_recording(self):
		if(self.recording_track_path == None):
			return
		self.send(f'loopFile {self.recording_track_path};\n')

	def pin_cb(self, button_pressed):
		#self.send(f'command {pin};\n')
		print(button_pressed)
		#if(pin == 4):
		#	self.get_next_file()
		#if(pin == 5):
		#	if(self.last_command == 'randomLoop'):
		#		self.send(f'command stopLoop;\n')
		#		self.last_command = 'stopLoop'
		#	elif(self.last_command == 'stopLoop'):
		#		self.send(f'command playLoop;\n')
		#		self.last_command = 'playLoop'
		#	elif(self.last_command == 'playLoop'):
		#		self.send(f'command stopLoop;\n')
		#		self.last_command = 'stopLoop'
		if(button_pressed == 'record'):
			self.start_recording()
		elif(button_pressed == 'play'):
			self.play_or_stop_file()
		elif(button_pressed == 'save'):
			self.save_current_file()
		elif(button_pressed == 'send'):
			self.send_current_file()
		elif(button_pressed == 'erase'):
			self.erase_current_file()
		elif(button_pressed == 'random'):
			self.get_next_file()

	def shuffle_pressed(self):
		self.get_next_file()

	def play_pressed(self):
		self.play_or_stop_file()

	def record_pressed(self):
		self.start_recording()

	def save_pressed(self):
		self.save_current_file()

	def send_pressed(self):
		self.send_current_file()

	def erase_pressed(self):
		self.erase_current_file()

	def run(self):
		while 1:
			data = self.receive_socket.recv(1024)
			print(data)
			self.parse_message(data.decode().strip())

	def start(self):
		self.button = Button(self.pin_cb)
		self.button.start_polling()
		t1 = threading.Thread(target=self.run)
		t1.start()

