# Status: Complete and working
# Description: Exports the following mentioned DynamoDB tables into csv in 'exports' directory
# How to: python3 export-dynamodb.py
# Note: Just update the TABLES array before running the script
import csv
from datetime import datetime
import pytz
import numpy as np
import json
import os

maindir = "averages"
if not os.path.exists(maindir):
    os.makedirs(maindir)

def get_attr_clips_dict():
    d = {}
    with open('exports/20210905160610-timbre_survey.csv', 'r', newline='')  as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if len(row['others']) <= 2:
                continue

            others = row['others'][1:-1]
            others = others.replace('\'', '')
            others = others.replace(' ', '')
            others = others.split(',')
            ans = row['answer']
            if ans not in ['clip_a', 'clip_b']:
                continue
            
            clip = row[ans]
            
            for o in others:
                if o in d:
                    d[o].append(clip)
                else:
                    d[o] = []
                    d[o].append(clip)
        return d

def get_name_vec_dict():
    filenames = []
    with open('embedding-filenames.tsv', 'r') as f:
        r = csv.reader(f, delimiter='\t')
        for row in r:
            filenames.append(row[0])
            # print(row)
    vec = []
    with open('embeddings.tsv', 'r') as f:
        r = csv.reader(f, delimiter='\t')
        for row in r:
            float_row = [float(i) for i in row]
            vec.append(float_row)
            # print(row)

    d_name_vec = {}
    for i in range(0, len(filenames)):
        d_name_vec[filenames[i].split(' ')[0]] = vec[i]

    return d_name_vec

def get_clip_short_to_long_name_dict():
    filenames = []
    d = {}
    with open('embedding-filenames.tsv', 'r') as f:
        r = csv.reader(f, delimiter='\t')
        for row in r:
            short = row[0].split(' ')[0]
            d[short] = row[0]
    return d


d_shorttolong_name = get_clip_short_to_long_name_dict()
json.dump(d_shorttolong_name, open("averages/dict_short_to_long_name.txt",'w'))

d_attr_clips = get_attr_clips_dict()
json.dump(d_attr_clips, open("averages/dict_attr_clips.txt",'w'))

d_name_vec = get_name_vec_dict()
json.dump(d_name_vec, open("averages/dict_name_vec.txt",'w'))




# print(d_name_vec)
d_attr_vecs = {}
all_embeddings = {}
contrast = ["Clean", "Bright", "Harsh"]
contrast_embeddings = {}
for k in d_attr_clips.keys():
    print(k)
    d_attr_vecs[k] = []
    clips = d_attr_clips[k]
    print(clips)
    for clip in clips:
        d_attr_vecs[k].append(d_name_vec[clip])
        all_embeddings[clip] = d_name_vec[clip]
        if k in contrast:
            contrast_embeddings[clip + "-" + k] = d_name_vec[clip]
    # print(d_attr_vecs)

    mean = list(np.mean(d_attr_vecs[k], axis = 0))
    all_embeddings[k + "-average"] = mean

    if k in contrast:
        contrast_embeddings[k + "-average"] = mean

    d_attr_vecs[k].append(mean)

    filedir = "averages/" + k + " - " + str(len(clips))
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    
    with open(os.path.join(filedir, "embeddings.tsv"), 'w', newline='') as f_output:
        tsv_output = csv.writer(f_output, delimiter='\t')
        tsv_output.writerows(d_attr_vecs[k])
    
    with open(os.path.join(filedir, "embeddings-filenames.tsv"), 'a') as f_output:
        f_output.seek(0)
        f_output.truncate()
        for clip in clips:
            f_output.write(clip)
            f_output.write('\n')
        f_output.write(k + "-average")

json.dump(d_attr_vecs, open("averages/dict_attr_vecs.txt",'w'))
json.dump(all_embeddings, open("averages/dict_all_embeddings.txt",'w'))
json.dump(contrast_embeddings, open("averages/dict_contrast_embeddings.txt",'w'))

with open(os.path.join(maindir, "all_embeddings.tsv"), 'w', newline='') as f_output:
    tsv_output = csv.writer(f_output, delimiter='\t')
    tsv_output.writerows(all_embeddings.values())

with open(os.path.join(maindir, "all_embeddings-filenames.tsv"), 'a') as f_output:
    f_output.seek(0)
    f_output.truncate()
    for clip in all_embeddings.keys():
        f_output.write(clip)
        f_output.write('\n')


with open(os.path.join(maindir, "contrast_embeddings.tsv"), 'w', newline='') as f_output:
    tsv_output = csv.writer(f_output, delimiter='\t')
    tsv_output.writerows(contrast_embeddings.values())

with open(os.path.join(maindir, "contrast_embeddings-filenames.tsv"), 'a') as f_output:
    f_output.seek(0)
    f_output.truncate()
    for clip in contrast_embeddings.keys():
        f_output.write(clip)
        f_output.write('\n')


