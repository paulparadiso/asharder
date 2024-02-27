from filer import *
from randomizer import *
from flask import Flask
from flask import request
from flask_cors import CORS
from flask import jsonify
from database import db_session
from models import Recording
from playsound import playsound

app = Flask(__name__)
CORS(app)

randomizer = None
current_project_name = None

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
			response[f.project].append({id: f.id, 'project': f.project, 'name': f.name, 'path': f.path})
		else:
			response[f.project] = [{'id': f.id, 'project': f.project, 'name': f.name, 'path': f.path}]
	print(response)
	return jsonify(response)

@app.route('/play', methods=['POST'])
def play_audio():
	data = request.json
	playsound('/home/patch/recordings/2023-12-7-6-25-15.wav')
	return "Playing"

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
