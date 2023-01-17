# Status: Complete and working
# Description: Exports the following mentioned DynamoDB tables into csv in 'exports' directory
# How to: python3 export-dynamodb.py
# Note: Just update the TABLES array before running the script
import csv
import boto3
from datetime import datetime
import pytz


TABLES = [
        'timbre_eval',
        'users',
        'timbre_survey',
        'dontknow',
        'less',
        'more',
        'notapplicable',
        'users-2'
        ]


def export_table(dynamodb, TABLE_NAME, ts):
    print('Exporting table: ' + TABLE_NAME)

    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    items = response['Items']

    print('\tDownloaded data for table: ' + TABLE_NAME + ' (' + str(len(items)) + ')')

    keys = set()
    for item in items: keys.update(item.keys())

    with open('exports-dynamo/' + ts + '-' + TABLE_NAME + '.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, list(keys))
        dict_writer.writeheader()
        dict_writer.writerows(items)


if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')

    timezone = pytz.timezone('Asia/Tokyo')
    now = timezone.localize(datetime.now())
    timestamp = now.strftime("%Y%m%d%H%M%S")
    print('Timestamp for the export: ' + timestamp)

    for table in TABLES:
        export_table(dynamodb, table, timestamp)

