from filer import *
from randomizer import *
from flask import Flask
from flask import request
from flask_cors import CORS
from flask import jsonify
from database import db_session
from models import Recording
from playsound import playsound
import shutil

app = Flask(__name__)
CORS(app)

randomizer = None
current_project_name = None

def add_file_to_loops(file_id):
	r = db_session.query(Recording).filter(Recording.id == file_id).first()
	shutil.copy(r.path, '/home/patch/loops')

@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

@app.route('/setparam', methods=['POST'])
def set_parameter():
	global randomizer
	data = request.json
	print(data)
	if(data['param'] == 'projectName'):
		randomizer.set_project_name(data['value'])
	randomizer.send(f'{data["param"]} {data["value"]};\n')
	return "Thanks"

@app.route('/files', methods=['GET'])
def get_files():
	response = {}
	files = Recording.query.all()
	for f in files:
		if(f.project in response):
			response[f.project].append({'id': f.id, 'project': f.project, 'name': f.name, 'path': f.path, 'upload': f.upload})
		else:
			response[f.project] = [{'id': f.id, 'project': f.project, 'name': f.name, 'path': f.path, 'upload': f.upload}]
	#print(response)
	return jsonify(response)

@app.route('/play', methods=['POST'])
def play_audio():
	data = request.json
	print(data)
	playsound(data['path'])
	return "Playing"

@app.route('/command', methods=['POST'])
def command():
	global randomizer
	data = request.json
	if data['command'] == 'randomLoop':
		randomizer.send(f'command 4;\n')
	if data['command'] == 'playLoop':
		randomizer.send(f'command 5;\n')
	if data['command'] == 'record':
		randomizer.send(f'command 15;\n')
	return "success"

@app.route('/updatefiles', methods=['POST'])
def update_files():
	data = request.json
	#print(data)
	for key in data['fileData']:
		r = db_session.query(Recording).filter(Recording.id == key).first()
		if "name" in data['fileData'][key]:
			r.name = data['fileData'][key]['name']
		if "upload" in data['fileData'][key]:
			r.upload = data['fileData'][key]['upload']
		db_session.commit()
		if "addLoop" in data['fileData'][key]:
			add_file_to_loops(key)
	return "Updated"

def on_message(msg):
	global comms
	print(msg)
	if(msg == 'get_random_file;'):
		comms.send('test.wav;')

def main():
	global randomizer
	randomizer = Randomizer('/home/pi/loops', 4445, 4446, db_session)
	randomizer.start()
	app.run(host='0.0.0.0')
	
if __name__ == "__main__":
	main()
