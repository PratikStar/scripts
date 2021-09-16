from typing import List, Optional

import random
import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr


dynamodb = boto3.resource('dynamodb')
survey_table = dynamodb.Table('timbre_survey')


ids = [
# "04c144a5-9d15-4691-ad79-e9c53a38133f",
# "190e35d9-ebf6-42ac-9038-298dc88b6f7f",
"19efb1d5-2191-4887-850d-160b7a5ea6a2",
"22b837ca-03dd-490f-8042-1e9fab096f14",
"3295539b-3f24-4d09-9807-7588f3001fe4",
"49c67282-4a6f-4b9f-a7ae-efd12781c247",
"70aa8fed-b440-4478-8219-9cc235335eda",
"825e1aa9-887b-4e6d-a38e-f7e1c652b13a",
"af1f6cd9-6fe2-4ca2-8346-a7a5009cfdc5",
"f9f88637-6104-4504-bf49-c9648ee3a2d1"]

for id1 in ids:
    print(id1)
    response = survey_table.scan(
        FilterExpression=Attr("user_id").eq(id1)
        )

    if 'Items' not in response:
        continue
    print(response['Items'])

    for row in response['Items']:

        survey_table.delete_item(
            Key=row['id'])

# ids = [
# "05b69fb2-e6ee-4555-b120-dcc3dec7bf67",
# "0dc79f48-f77a-43fe-acbc-b147add5dd67",
# "1b132932-0da2-4ac2-bea7-03eff644e981",
# "2a2fbca4-2dcc-4798-ad05-252374635459",
# "2e8b548a-bbe7-4070-bd7a-9bd859a25ab4",
# "56f1c00f-9be0-4713-8b8a-5f516ad81825",
# "5cc707f1-de11-4867-9e53-c95b19bdf064",
# "5dd5449b-ac9f-4ce6-8a1d-49a752c8d5bd",
# "5e4ab72a-57d1-4306-93ab-f661d1f1c2ea",
# "8f3348aa-b95b-4f4b-a1b0-d0c91f37e71a",
# "9d2e7bd3-a451-4788-8d26-190a35654272",
# "b3122d87-464e-4835-98b3-de46ad80e43e",
# "becb0280-b2c9-42f2-af54-efd0db0b774c",
# "c8cf0af6-2413-4dab-86ec-3284fde536a7",
# "d2a29c01-63fe-4c12-9a5d-d1d1131ca1ad",
# "d7a61861-f839-4d8c-8d32-4c96db1dd1e5",
# "f3147591-6eef-47ff-8685-9798db149891",
# "f68fb3a2-640c-4154-8c11-239a774a3e6c"]


# for id1 in ids:

#     survey_table.update_item(
#         Key={'id': id1},
#         UpdateExpression="set user_id = :g",
#         ExpressionAttributeValues={
#             ':g': 'f6620e43-6cb4-4bde-9d92-9c61f842bfdd'
#         },
#         ReturnValues="UPDATED_NEW"
#     )

