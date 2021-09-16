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

a = []


response = survey_table.scan(
    # FilterExpression=Attr("email").eq("sihyun06@gmail.com")
    )
print("Downloaded Survey data...\n")

count = 0
t = 0
for row in response['Items']:
    if row['others'] is not None and len(row['others']) != 0:
        a.append(row['others'])
        count += len(row['others'])
        t += 1

print(str(a))
print(count)
print(t)
