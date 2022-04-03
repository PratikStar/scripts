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
import utilities
from scipy import spatial

### Export data ---do something---> output

exports_dynamo_directory = "../exports-dynamo"
exports_drive_directory = "../exports-drive"

if not os.path.exists("dicts"):
    os.makedirs("dicts")
if not os.path.exists("tsv"):
    os.makedirs("tsv")

################################
################################

d_attribute_to_clipids = utilities.get_attribute_to_clipids_dict(exports_dynamo_directory)
# json.dump(d_attribute_to_clipids, open("dicts/dict_attribute_to_clipids.txt",'w'))

################################
################################

d_clipid_to_embedding = utilities.get_clipid_to_embedding_dict(exports_drive_directory)
# json.dump(d_clipid_to_embedding, open("dicts/dict_clipid_to_embedding.txt",'w'))

################################
################################

d_clipid_to_clipname = utilities.get_clipid_to_clipname_dict()
# json.dump(d_clipid_to_clipname, open("dicts/dict_clipid_to_clipname.txt",'w'))
################################
################################

d_attribute_to_embeddings = utilities.get_attribute_to_embeddings_dict(exports_dynamo_directory, exports_drive_directory)
json.dump(d_attribute_to_embeddings, open("dicts/dict_attribute_to_embeddings.txt",'w'))

# this function assumes that the mean embeddings are calculated
def get_mean_embeddings_dict():
    path = os.path.join("dicts", "dict_mean_embeddings.txt")
    if os.path.isfile(path):
        return utilities.get_as_dict(path)

def calculate_and_save_mean_embeddings_in_separate_dirs(d_attribute_to_clipids, path = "mean_embeddings"):
    mean_embeddings = {}

    for attribute, clipids in d_attribute_to_clipids.items():

        embeddings = []
        for clipid in clipids:
            subembeddings = []
            for windowed_clipid in d_clipid_to_embedding.keys():
                if clipid == windowed_clipid[0:8]:
                    subembeddings.append(d_clipid_to_embedding[windowed_clipid])
            embeddings.append(list(np.mean(subembeddings, axis = 0)))
        mean = list(np.mean(embeddings, axis = 0))

        mean_embeddings["avg-" + attribute] = mean

        filedir = path + "/" + attribute + " - " + str(len(clipids))
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        
        with open(os.path.join(filedir, "embeddings.tsv"), 'w', newline='') as f_output:
            tsv_output = csv.writer(f_output, delimiter='\t')
            tsv_output.writerows(embeddings)
            tsv_output.writerow(mean)
        
        with open(os.path.join(filedir, "embeddings-filenames.tsv"), 'a') as f_output:
            f_output.seek(0)
            f_output.truncate()
            for clipid in clipids:
                f_output.write(clipid)
                f_output.write('\n')
            f_output.write("avg-" + attribute)
    return mean_embeddings

d_mean_embeddings = calculate_and_save_mean_embeddings_in_separate_dirs(d_attribute_to_clipids, "mean")
json.dump(d_mean_embeddings, open("dicts/dict_mean_embeddings.txt",'w'))


# For mean + clip embeddings
all_embeddings = {**d_mean_embeddings, **d_clipid_to_embedding}
json.dump(all_embeddings, open("dicts/dict_all_attribute_to_embeddings.txt",'w'))


### The same embeddings as tsv files
with open(os.path.join("tsv", "all_embeddings.tsv"), 'w', newline='') as f_output:
    tsv_output = csv.writer(f_output, delimiter='\t')
    tsv_output.writerows(all_embeddings.values())

with open(os.path.join("tsv", "all_embeddings-filenames.tsv"), 'a') as f_output:
    f_output.seek(0)
    f_output.truncate()
    for clip in all_embeddings.keys():
        f_output.write(clip)
        f_output.write('\n')


def calculate_distances_from_given_point(input_embedding, d_clipid_to_embedding):

    distances = {}
    for clipid, embedding in d_clipid_to_embedding.items():
        if len(input_embedding) != len(embedding):
            print("incompatiple points")
            return
        distance = spatial.distance.cosine(input_embedding, embedding)
        distances[clipid] = distance
    return distances

# d_clipid_to_embedding = utilities.get_clipid_to_embedding_dict(exports_drive_directory)
# distances = calculate_distances_from_given_point([-6.388096879999998, 0.377319869, 1.1479962568, -5.205606348, -5.966678312, 6.881093943999998, -2.7488120604, -5.864104612], d_clipid_to_embedding)




def get_distances_from_given_attribute(input_attribute, d_clipid_to_embedding):

    mean_embeddings = get_mean_embeddings_dict()
    if 'avg-' + input_attribute  not in mean_embeddings:
        print(input_attribute + "not in mean_embeddings dict")
    input_attribute_embedding = mean_embeddings['avg-' + input_attribute]

    distances = {}
    for clipid, embedding in d_clipid_to_embedding.items():

        distance = spatial.distance.cosine(input_attribute_embedding, embedding)
        distances[clipid] = distance
    return distances

def get_top_n_elements_by_dict_value(d, n):
    sorted_dict = dict(sorted(d.items(), key = lambda x: x[1], reverse = False))
    # print(list(sorted_dict))
    return {k: sorted_dict[k] for k in list(sorted_dict)[:n]}






############### Driver ##################
# d_clipid_to_embedding = utilities.get_clipid_to_embedding_dict(exports_drive_directory)
# distances_from_attribute = get_distances_from_given_attribute('Brittle', d_clipid_to_embedding)
# top_n_closest_clipids = get_top_n_elements_by_dict_value(distances_from_attribute, 5)

# d_clipid_to_clipname = utilities.get_clipid_to_clipname_dict()
# clips = [d_clipid_to_clipname[k] for k in top_n_closest_clipids.keys()]
# print(clips)
######################################


filenames = []
with open(os.path.join("../exports-drive", "embedding-testing-filenames.tsv"), 'r') as f:
    r = csv.reader(f, delimiter='\t')
    for row in r:
        filenames.append(row[0])
        # print(row)
vec = []


with open(os.path.join("../exports-drive", "embeddings-testing.tsv"), 'r') as f:
    r = csv.reader(f, delimiter='\t')
    for row in r:
        float_row = [float(i) for i in row]
        vec.append(float_row)
        # print(row)

d_name_vec = {}
for i in range(0, len(filenames)):
    d_name_vec[filenames[i].split(' ')[0]] = vec[i]

print(d_name_vec)

attrs_32 = ["Aggressive", "Bright", "Compressed", "Crunchy", "Distorted", "Round", "Thick"]
attrs_25 = ["Abrasive", "Aggressive", "Bright", "Buzzy", "Compressed", "Crunchy", "Dark", "Distorted", "Fizzy", "Fuzzy", "Gritty", "Muffled", "Round", "Saturated", "Thick", ""]
# attrs = ["Clean" , "Twangy" , "Distorted" , "Crushing" , "Chunky" , "Aggressive" , "Bright" , "Compressed"]



for attr in attrs_32:

    distances_from_attribute = get_distances_from_given_attribute(attr, d_name_vec)
    top_n_closest_clipids = get_top_n_elements_by_dict_value(distances_from_attribute, 20)

    # print(top_n_closest_clipids.keys())
    print("--- " + attr + " ---")
    for k in top_n_closest_clipids.keys():
        print('\t' + k.split('.')[0])














# d_attribute_to_embeddings = {}
# all_embeddings = {}
# contrast = ["Clean", "Bright", "Harsh"]
# contrast_embeddings = {}
# for k in d_attribute_to_clipids.keys():
#     print(k)
#     d_attribute_to_embeddings[k] = []
#     clips = d_attribute_to_clipids[k]
#     print(clips)
#     for clip in clips:
#         d_attribute_to_embeddings[k].append(d_clipid_to_embedding[clip])
#         all_embeddings[clip] = d_clipid_to_embedding[clip]
#         if k in contrast:
#             contrast_embeddings[clip + "-" + k] = d_clipid_to_embedding[clip]
#     # print(d_attribute_to_embeddings)

#     mean = list(np.mean(d_attribute_to_embeddings[k], axis = 0))
#     all_embeddings[k + "-average"] = mean

#     if k in contrast:
#         contrast_embeddings[k + "-average"] = mean

#     d_attribute_to_embeddings[k].append(mean)

#     filedir = "averages/" + k + " - " + str(len(clips))
#     if not os.path.exists(filedir):
#         os.makedirs(filedir)
    
#     with open(os.path.join(filedir, "embeddings.tsv"), 'w', newline='') as f_output:
#         tsv_output = csv.writer(f_output, delimiter='\t')
#         tsv_output.writerows(d_attribute_to_embeddings[k])
    
#     with open(os.path.join(filedir, "embeddings-filenames.tsv"), 'a') as f_output:
#         f_output.seek(0)
#         f_output.truncate()
#         for clip in clips:
#             f_output.write(clip)
#             f_output.write('\n')
#         f_output.write(k + "-average")

# json.dump(d_attribute_to_embeddings, open("averages/dict_attr_vecs.txt",'w'))
# json.dump(all_embeddings, open("averages/dict_all_embeddings.txt",'w'))
# json.dump(contrast_embeddings, open("averages/dict_contrast_embeddings.txt",'w'))

# with open(os.path.join("averages", "all_embeddings.tsv"), 'w', newline='') as f_output:
#     tsv_output = csv.writer(f_output, delimiter='\t')
#     tsv_output.writerows(all_embeddings.values())

# with open(os.path.join("averages", "all_embeddings-filenames.tsv"), 'a') as f_output:
#     f_output.seek(0)
#     f_output.truncate()
#     for clip in all_embeddings.keys():
#         f_output.write(clip)
#         f_output.write('\n')


# with open(os.path.join("averages", "contrast_embeddings.tsv"), 'w', newline='') as f_output:
#     tsv_output = csv.writer(f_output, delimiter='\t')
#     tsv_output.writerows(contrast_embeddings.values())

# with open(os.path.join("averages", "contrast_embeddings-filenames.tsv"), 'a') as f_output:
#     f_output.seek(0)
#     f_output.truncate()
#     for clip in contrast_embeddings.keys():
#         f_output.write(clip)
#         f_output.write('\n')


