#!/usr/bin/python3

from database import db_session
from models import Recording
import pathlib
import os
import glob

def run():
	recordings = db_session.query(Recording).all()
	for r in recordings:
		file = pathlib.Path()
		if(file.is_file()):
			print(f'Deleting {file}')
			file.unlink()
		db_session.delete(r)
	db_session.commit()
	files = glob.glob('/home/patch/recordings/*')
	for f in files:
		os.remove(f)
	
if __name__ == '__main__':
	run()
