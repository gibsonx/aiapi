import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aiapi.settings")
django.setup()
from django.conf import settings
from utils.S3 import S3
import boto3
import logging

if __name__ == "__main__":
    aws_access_key_id = settings.S3_SECRET_ID
    aws_secret_access_key = settings.S3_SECRET_KEY
    endpoint_url = settings.S3_ENDPOINT_URL
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  endpoint_url=endpoint_url)

    session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    s3 = session.resource('s3',endpoint_url=endpoint_url)
    my_bucket = s3.Bucket('aspine-ai')

    for obj in my_bucket.objects.all():
        if obj.key.endswith('jpg'):
            print(obj.key)