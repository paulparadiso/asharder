import boto3

audio_dir = '/home/patch/reacordings'

session = boto3.Session(profile_name='default')
s3_resource = session.resource('s3')

ash_bucket_name = 'asharder-bucket'
file_name = '/home/patch/recordings/1.wav'

s3_resource.Object(ash_bucket_name, file_name).upload_file(Filename=file_name)

def create_session():
    pass

def upload_file(project_name, file_name):
    create_session()

 