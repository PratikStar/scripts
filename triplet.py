from typing import List, Optional

import random
import csv
import boto3
import uuid
import pytz
from datetime import datetime, timezone, timedelta
from boto3.dynamodb.conditions import Key, Attr
import constants

dynamodb = boto3.resource('dynamodb')
survey_table = dynamodb.Table('timbre_survey')


more = {}
for attr in constants.attributes:
    more[attr] = {'more': {}, 'less': {}}

response = survey_table.scan(
    # FilterExpression=Attr("email").eq("sihyun06@gmail.com")
    )

print("Downloaded Survey data...\n")


f = {}
for attr in constants.attributes:
    f[attr] = {}


for row in response['Items']:
    if row['answer'] == 'na':
        # print(row)
        continue
    if row['answer'] == 'dontknow':
        # print(row)
        continue


    if row['answer'] == 'clip_a':

        if row['clip_a'] not in f[row['attribute']]:
            f[row['attribute']][row['clip_a']] = [row['clip_b']]
        else:
            f[row['attribute']][row['clip_a']].append(row['clip_b'])

    if row['answer'] == 'clip_b':

        if row['clip_b'] not in f[row['attribute']]:
            f[row['attribute']][row['clip_b']] = [row['clip_a']]
        else:
            f[row['attribute']][row['clip_b']].append(row['clip_a'])


with open('link.csv', 'w') as file:  # You will need 'wb' mode in Python 2.x
    file.write(str(f))



for attr in f:
    for winclip in f[attr]:
        for looseclip in f[attr][winclip]:
            if looseclip in f[attr]:
                print(attr)
                print(winclip)
                print(attr + ": " + winclip + " > " + looseclip + " > " + str(f[attr][looseclip]) + "\n")

