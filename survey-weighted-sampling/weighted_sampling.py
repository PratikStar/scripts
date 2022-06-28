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


def put_to_na(row):
    if row['clip_a'] not in na[row['attribute']]:
        na[row['attribute']][row['clip_a']] = 1
    else:
        na[row['attribute']][row['clip_a']] += 1

    if row['clip_b'] not in na[row['attribute']]:
        na[row['attribute']][row['clip_b']] = 1
    else:
        na[row['attribute']][row['clip_b']] += 1

def put_to_dontknow(row):
    if row['clip_a'] not in dontknow[row['attribute']]:
        dontknow[row['attribute']][row['clip_a']] = 1
    else:
        dontknow[row['attribute']][row['clip_a']] += 1

    if row['clip_b'] not in dontknow[row['attribute']]:
        dontknow[row['attribute']][row['clip_b']] = 1
    else:
        dontknow[row['attribute']][row['clip_b']] += 1


na = {}
for attr in constants.attributes:
    na[attr] = {}

dontknow = {}
for attr in constants.attributes:
    dontknow[attr] = {}

more = {}
for attr in constants.attributes:
    more[attr] = {}

less = {}
for attr in constants.attributes:
    less[attr] = {}

response = survey_table.scan(
    # FilterExpression=Attr("email").eq("sihyun06@gmail.com")
    )

print("Downloaded Survey data...\n")

for row in response['Items']:
    if row['others'] is None or row['others'] == []:
        continue

    qchanged = datetime(2021, 7, 19, 17, 19, 0, tzinfo=timezone.utc) # In JST
    
    ansclip = 'clip_a'
    if datetime.strptime(row['reg_ts'], '%a %b %d %H:%M:%S %Y').replace(tzinfo=pytz.timezone('Japan')) > qchanged and row['answer'] == 'clip_b': # Tue Jul 20 10:39:37 2021
        ansclip = row['answer']

    for attr in row['others']:
        if row[ansclip] not in more[attr]:
            more[attr][row[ansclip]] = 1
        else:
            more[attr][row[ansclip]] += 1

print("Loaded the other tags data...\n")

for row in response['Items']:
    if row['answer'] == 'na':
        # print(row)
        put_to_na(row)
        continue
    if row['answer'] == 'dontknow':
        # print(row)
        put_to_dontknow(row)
        continue
    if row['answer'] == 'clip_a':

        if row['clip_a'] not in more[row['attribute']]:
            more[row['attribute']][row['clip_a']] = 1
        else:
            more[row['attribute']][row['clip_a']] += 1

        if row['clip_b'] not in less[row['attribute']]:
            less[row['attribute']][row['clip_b']] = 1
        else:
            less[row['attribute']][row['clip_b']] += 1
        continue

    if row['answer'] == 'clip_b':

        if row['clip_b'] not in more[row['attribute']]:
            more[row['attribute']][row['clip_b']] = 1
        else:
            more[row['attribute']][row['clip_b']] += 1

        if row['clip_a'] not in less[row['attribute']]:
            less[row['attribute']][row['clip_a']] = 1
        else:
            less[row['attribute']][row['clip_a']] += 1
        continue

print("Created more, less and na, arrays...\n")

## Creating features Table

features = {}

for i in range(1, constants.CLIPS_NUM+1):
    for j in range(1, 13):
        clip_id = ('%05d' % i) + "-" + ('%02d' % j)
        features[clip_id] = {}

        for attr in constants.attributes:
            features[clip_id][attr] = 10

            # About More
            if clip_id in more[attr]:
                features[clip_id][attr] += more[attr][clip_id]

            # Less
            if clip_id in less[attr]:
                features[clip_id][attr] -= less[attr][clip_id]

            # NA
            if clip_id in na[attr]:
                features[clip_id][attr] -= (na[attr][clip_id] * 2)

print("Created features array...\n")


with open('mycsvfile.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
    w = csv.DictWriter(f, features.keys())
    w.writeheader()
    w.writerow(features)

csv = []
for k in features:
    csv.append(list(features[k].values()))

with open('features.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
    for row in csv:
        string_ints = [str(i) for i in row]
        f.write(",".join(string_ints) + "\n")















print("===========================\n\n\n")
print(na)
print("===========================\n\n\n")
print(dontknow)
print("===========================\n\n\n")
print(less)
print("===========================\n\n\n")
print(more)
print("===========================\n\n\n")


print("Now inserting...")

na_table = dynamodb.Table('notapplicable')
dontknow_table = dynamodb.Table('dontknow')
more_table = dynamodb.Table('more')
less_table = dynamodb.Table('less')


with na_table.batch_writer() as batch:
    for attr in constants.attributes:
        batch.put_item(
            Item={
                'attribute': attr,
                'weights': na[attr]
            }
        )

with dontknow_table.batch_writer() as batch:
    for attr in constants.attributes:
        batch.put_item(
            Item={
                'attribute': attr,
                'weights': dontknow[attr]
            }
        )
with less_table.batch_writer() as batch:
    for attr in constants.attributes:
        batch.put_item(
            Item={
                'attribute': attr,
                'weights': less[attr]
            }
        )
with more_table.batch_writer() as batch:
    for attr in constants.attributes:
        batch.put_item(
            Item={
                'attribute': attr,
                'weights': more[attr]
            }
        )
