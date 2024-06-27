from database import db_session
from models import Recording
import pathlib

def run():
	recordings = db_session.query(Recording).all()
    for r in recordings:
		if not r.upload:
			db_session.delete(r)
			file = pathlib.Path()
			if(file.is_file()):
				file.unlink()
	db_session.commit()
	
if __name__ == '__main__':
	run()
