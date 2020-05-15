import sys
import csv
import codecs
import requests
import os
import tempfile

from google.cloud import storage


def main(request):
    # Spreadsheet Web application URL
    url = 'https://script.google.com/macros/s/AKfycbx9YwMQpTU_nu5k1mfx1SNigsP5fH_3i6Y55xPJny3XAftsR1s/exec'

    # Cloud Storage
    # if local, comment in
    # gcpCredential = 'credentials/bbp-db.json'
    bucket = 'bbp-original-db-storage'
    dir = 'test'
    fileName = 'music.csv'

    # get data
    r = requests.get(url)
    assert r.status_code == requests.codes.ok, "can't read spreadsheet"  # pylint: disable=no-member

    # make file
    _, temp_local_filename = tempfile.mkstemp()
    with codecs.open(temp_local_filename, 'w', 'utf_8') as f:
        f.write(r.text)

    # upload file
    # if local, comment in
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcpCredential
    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.blob(f'{dir}/{fileName}')
    blob.upload_from_filename(filename=temp_local_filename)
    blob.content_type = 'text/csv'
    blob.cache_control = 'no-cache'
    blob.patch()
    return "success"
