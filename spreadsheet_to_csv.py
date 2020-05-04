import csv
import codecs
import requests
import os
from google.cloud import storage

url = 'https://script.google.com/macros/s/AKfycbx9YwMQpTU_nu5k1mfx1SNigsP5fH_3i6Y55xPJny3XAftsR1s/exec'

response = requests.get(url)

# print(response.text)

# print(response)
# <Response [200]>

# print(type(response))

# <class 'requests.models.Response'>

tmp = 'tmp'
fileName = 'music.csv'
if not os.path.exists(tmp):
    os.makedirs(tmp)

path = f'{tmp}/{fileName}'
with codecs.open(path, 'w', 'utf_8') as f:
    f.write(response.text)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'credencials/bbp-db.json'
client = storage.Client()
bucket = client.get_bucket('bbp-original-db-storage')
blob = bucket.blob(f'test/{fileName}')
blob.upload_from_filename(filename=f'{tmp}/{fileName}')
for f in bucket.list_blobs():
    print(f)
