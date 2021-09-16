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

allcount = {}
answered = {}
for attr in constants.attributes:
    allcount[attr] = 0
    answered[attr] = 0

response = survey_table.scan(
    # FilterExpression=Attr("email").eq("sihyun06@gmail.com")
    )
print("Downloaded Survey data...\n")


for row in response['Items']:
    if row['answer'] == 'na' or row['answer'] == 'dontknow':
        allcount[row['attribute']] += 1
    else:
        allcount[row['attribute']] += 1
        answered[row['attribute']] += 1

print(allcount)
print(answered)

with open("timbre_survey_dict.txt", 'w') as file:
    for key in allcount:
        file.write(str(key) + " " + str(allcount[key]) + "\n")

with open("timbre_survey_ans_dict.txt", 'w') as file:
    for key in answered:
        file.write(str(key) + " " + str(answered[key]) + "\n")
