# Status: In progress
# Description: 
# How to: python3 <>.py
# Note: Just update the TABLES array before running the script
import csv
from datetime import datetime
import pytz
import numpy as np
import json
import os
import os.path
from scipy import spatial
import pandas as pd
import pprint
### Export data ---do something---> output

exports_dynamo_directory = "../exports-dynamo"
exports_drive_directory = "../exports-drive"

if not os.path.exists("dicts"):
    os.makedirs("dicts")
if not os.path.exists("tsv"):
    os.makedirs("tsv")

################################
################################


def get_clip_to_attribute_df(exports_dynamo_directory = "../exports-dynamo"):
    d = {} ## clip -> attribute
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), exports_dynamo_directory, '20210905160610-timbre_survey.csv'), 'r', newline='')  as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            # print('\n ======= ')
            # print(row)

            ## The person has not actually listened
            # if len(row['clicks']) == 0:
            #     print('Unclicked annotation')
            #     continue
            
            ## The 'others' string is empty
            ## Note: row['others'] is a string
            if len(row['others']) <= 2:
                continue

            ans = row['answer']
            ## The answer is 'Not Applicable'
            if ans not in ['clip_a', 'clip_b']:
                continue
            clip = row[ans]

            attributes = row['others'][1:-1].replace('\'', '').replace(' ', '').split(',')
            
            
            
            for attribute in attributes:
                if clip in d:
                    if attribute in d[clip]:
                        d[clip][attribute] += 1
                    else:
                        d[clip][attribute] = 1
                else:
                    d[clip] = {}
                    d[clip][attribute] = 1
            # break

    ## Print the dictionary
    with open(os.path.join('dicts', 'd_clip_to_attribute_to_count.txt'), 'wt') as out:
        pprint.pprint(d, stream=out, indent=4, width=20)

    df = pd.DataFrame.from_dict(data=d)
    df = df.T # transpose the DF, Now, rows -> clips, columns -> attributes
    
    # print(df)
    return df

# df = get2dmatrix()
# print(df.loc[['Distorted'] , ['00018-10', '00003-11']])