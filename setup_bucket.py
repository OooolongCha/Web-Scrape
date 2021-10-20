# https://www.youtube.com/watch?v=pEbL_TT9cHg

import os 
from google.cloud import storage 

os.chdir('S:\\NUS\\EBAC5006 Project\\GCP Streaming')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ServiceKey.json'

storage_client = storage.Client()


'''
Create a new bucket
'''
bucket_name = 'data5006'
bucket = storage_client.bucket(bucket_name)
# bucket.location = 'US'
bucket = storage_client.create_bucket(bucket)

vars(bucket)


'''
Accessing a specific bucket
'''
my_bucket = storage_client.get_bucket('data5006')


'''
Upload files
'''

def upload_to_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket('data5006')
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False

file_path = r''
upload_to_bucket()


'''
Dowload files
'''
def download_file_from_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket('data5006')
        blob = bucket.blob(blob_name)
        with open(file_path, 'wb') as f:
            storage_client.download_blob_to_file(blob, f)
        return True
    except Exception as e:
        print(e)
        return False
    