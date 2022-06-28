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

response = survey_table.scan(
    # FilterExpression=Attr("email").eq("sihyun06@gmail.com")
    )

print("Downloaded Survey data...\n")


f = {}

for row in response['Items']:
    c = [row['clip_a'], row['clip_b']]
    c = sorted(c)
    s = row['attribute'] + "--" + c[0] + "--" + c[1]
    
    if s not in f:
        f[s] = 1
    else:
        print(s)
        print(row)


with open('interannotatordist.csv', 'w') as file:  # You will need 'wb' mode in Python 2.x
    file.write(str(f))


