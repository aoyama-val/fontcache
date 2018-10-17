from __future__ import print_function
import subprocess

import sys
import os
import base64
import boto3
import logging
from os.path import join

logger = logging.getLogger()  
logger.setLevel(logging.INFO)  

BUCKET_NAME = 'aoyama.vallab.ninja'

def lambda_handler(event, context):
    os.environ['FONTCONFIG_PATH'] = '/var/task/fonts'
    try:
        os.makedirs('/tmp/fonts-cache', exist_ok=True)
    except OSError as e:
        (errno, strerror) = e
        print('OSError {}'.format(strerror))

    args = [ 'fc-cache', '-v', '/var/task/fonts' ]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    returncode = p.returncode
    stdout_data, stderr_data = p.communicate()

    print('stdout_data:\n' + stdout_data.decode('utf-8'))
    print('stderr_data:\n' + stderr_data.decode('utf-8'))
    s3bucket = boto3.resource('s3').Bucket(BUCKET_NAME)
    tmp_fontconfig = '/tmp/fonts-cache'
    for cache in os.listdir(tmp_fontconfig):
        response = s3bucket.upload_file(join(tmp_fontconfig, cache), cache)
        print("Uploaded " + cache)
        with open(join(tmp_fontconfig, cache), mode='rb') as f:
            print("{}:\n{}\n".format(cache, base64.b64encode(f.read())))
