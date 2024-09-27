#!/usr/bin/python3

from database import db_session
from models import Recording
import pathlib

def run():
	recordings = Recording.query.all()
	for r in recordings:
		print(r)
		if not r.upload:
			file = pathlib.Path(r.path)
			if(file.is_file()):
				print(f'Deleting {file}')
				file.unlink()
			db_session.delete(r)
	db_session.commit()
	
if __name__ == '__main__':
	run()
