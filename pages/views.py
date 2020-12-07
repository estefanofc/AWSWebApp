import boto3
import os
from django.utils.functional import keep_lazy
import requests

from boto3.dynamodb.conditions import Key
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.template.response import TemplateResponse

AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY


class HomePageView(TemplateView):
    template_name = 'home.html'


def process_data(data):
    f_name = 'input.txt'
    # Save data to file
    file = open(f_name, "r")
    f_lines = file.readlines()
    separated_list = []
    for line in f_lines:
        separated_list.append(line.split())
    mapped_data = []
    for entry in separated_list:
        map_entry = {}
        map_entry['last_name'] = entry[0]
        map_entry['first_name'] = entry[1]
        for index in range(2, len(entry)):
            pair = entry[index].split('=')
            map_entry[pair[0]] = pair[1]
        mapped_data.append(map_entry)
    file.close()
    return mapped_data


def load(request):
    # ----------------------S3----------------------
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

    # ----------------------DynamoDB----------------------
    mapped_data = process_data(data)
    table_name = 'program4table'
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='us-west-1',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    table = dynamodb.Table(table_name)
    # Input items
    for map in mapped_data:
        table.put_item(Item=map)
    return redirect(reverse('home'))


def clear(request):
    # ----------------------S3----------------------
    # Connect to bucket
    bucket_name = 'program4bucket'
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
    # delete s3 object
    bucket = s3.Bucket(bucket_name)
    bucket.objects.all().delete()
    # ----------------------DynamoDB----------------------
    table_name = 'program4table'
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='us-west-1',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    table = dynamodb.Table(table_name)
    scan = table.scan()
    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(Key={
                'last_name': each['last_name'],
                'first_name': each['first_name']
            })

    return redirect(reverse('home'))


def query(request):
    table_name = 'program4table'
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='us-west-1',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    table = dynamodb.Table(table_name)
    first_name = request.POST.get('first_name', 'default1')
    last_name = request.POST.get('last_name', 'default2')
    map = {}
    if first_name == '' and last_name == '':
        map['content'] = 'Please fill out at least one field'
        return TemplateResponse(request, 'home.html', map)
    if first_name == '':
        try:
            map['content'] = table.query(
                KeyConditionExpression=Key('last_name').eq(last_name)).get(
                    'Items', {})
        except Exception as e:
            map['content'] = str(e)
        if not map['content']:
            map['content'] = 'No data matching query found'
        return TemplateResponse(request, 'home.html', map)
    if last_name == '':
        try:
            map['content'] = table.query(
                IndexName='first_name-last_name-index',
                KeyConditionExpression=Key('first_name').eq(first_name)).get(
                    'Items', {})
        except Exception as e:
            map['content'] = str(e)
        if not map['content']:
            map['content'] = 'No data matching query found'
        return TemplateResponse(request, 'home.html', map)

    map['content'] = table.get_item(Key={
        'last_name': last_name,
        'first_name': first_name,
    }).get('Item', {})
    if not map['content']:
        map['content'] = 'No data matching query found'
    return TemplateResponse(request, 'home.html', map)
