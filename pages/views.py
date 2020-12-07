import boto3
import os
import requests

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY


class HomePageView(TemplateView):
    template_name = 'home.html'


def load(request):
    # Get data from URL
    URL = 'https://s3-us-west-2.amazonaws.com/css490/input.txt'
    f_name = 'input.txt'
    req = requests.get(URL)
    data = req.text
    # Save data to file
    file = open(f_name, "w+")
    file.write(data)
    file.seek(0)
    # Connect to bucket
    bucket_name = 'program4bucket'
    full_path = os.getcwd()
    s3 = boto3.resource(
        's3',
        region_name='us-west-1',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    b_exists = s3.Bucket(bucket_name).creation_date is not None
    if not b_exists:
        try:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': 'us-west-1'})
            print(bucket_name + ' created!')
        except Exception as e:
            print(e)
            return redirect(reverse('home'))
    # upload object
    s3.Object(bucket_name,
              f_name).put(Body=open(os.path.join(full_path, f_name), 'rb'))
    # close file
    print("Uploading File: " + "\t" + os.path.join(full_path, f_name))
    file.close()

    return redirect(reverse('home'))


def clear(request):
    print("CLEAR")
    return redirect(reverse('home'))
