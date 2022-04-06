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


def get_subclip_vs_attribute_df(exports_dynamo_directory = "../exports-dynamo"):
    d = {} ## subclip -> attribute
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
            subclip = row[ans]

            attribute = row['attribute']


            if row['clip_a'] not in d:
                d[row['clip_a']] = {}
                d[row['clip_a']][attribute] = 1 if ans == 'clip_a' else -1
            else:
                if attribute not in d[row['clip_a']]:
                    d[row['clip_a']][attribute] = 1 if ans == 'clip_a' else -1
                else:
                    if ans == 'clip_a':
                        d[row['clip_a']][attribute] += 1
                    else:
                        d[row['clip_a']][attribute] -= 1

            if row['clip_b'] not in d:
                d[row['clip_b']] = {}
                d[row['clip_b']][attribute] = 1 if ans == 'clip_b' else -1
            else:
                if attribute not in d[row['clip_b']]:
                    d[row['clip_b']][attribute] = 1 if ans == 'clip_b' else -1
                else:
                    if ans == 'clip_b':
                        d[row['clip_b']][attribute] += 1
                    else:
                        d[row['clip_b']][attribute] -= 1




            # Processing "others"
            attributes = row['others'][1:-1].replace('\'', '').replace(' ', '').split(',')
            
            for attribute in attributes:
                if subclip in d:
                    if attribute in d[subclip]:
                        d[subclip][attribute] += 1
                    else:
                        d[subclip][attribute] = 1
                else:
                    d[subclip] = {}
                    d[subclip][attribute] = 1
            # break

    ## Print the dictionary
    with open(os.path.join('dicts', 'd_subclip_to_attribute_to_count.txt'), 'wt') as out:
        pprint.pprint(d, stream=out, indent=4, width=20)

    df = pd.DataFrame.from_dict(data=d)
    df = df.T # transpose the DF, Now, rows -> subclips, columns -> attributes
    
    # print(df)
    return df

df = get_subclip_vs_attribute_df()



# Input to this will be clips x attributes dataframe. Using get_subclip_vs_attribute_df
def get_attribute_to_min_max_clips_dict(df):
    d = {}
    for (attribute, subclips) in df.iteritems():
        # print(attribute)
        # print(subclips)
        d[attribute] = {}
        for subclip, count in subclips.items():
            if pd.notnull(count):
                d[attribute][subclip] = count
                # print(subclip)
                # print(count)
    ## Print the dictionary
    with open(os.path.join('dicts', 'd_attribute_to_subclip_to_count.txt'), 'wt') as out:
        pprint.pprint(d, stream=out, indent=4, width=20)
    return d

pprint.pprint(get_attribute_to_min_max_clips_dict(df))

