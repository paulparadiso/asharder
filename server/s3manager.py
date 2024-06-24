import boto3
from database import db_session
from models import Recording
import os.path

AUIDIO_DIR = '/home/patch/reacordings'
BUCKET_NAME = 'asharder-bucket'

#def upload_file(project_name, file_name):
#    

def upload_files():
    session = boto3.Session(profile_name='default')
    s3_resource = session.resource('s3')
    recordings = db_session.query(Recording).all()
    for r in recordings:
        if r.upload and not r.uploaded:
            if os.path.exists(r.path):
                print(f'uploading {r.name}')
                upload_name = r.name
                if '.wav' not in upload_name:
                    upload_name += '.wav'
                s3_resource.Object(BUCKET_NAME, r.project + '/' + r.name).upload_file(Filename=r.path, ExtraArgs={'ContentDisposition': f'attachment;filename="{upload_name}"'})
                r.uploaded = True
                db_session.commit()

if __name__ == '__main__':
    upload_files()
    