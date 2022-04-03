import csv
from datetime import datetime
import pytz
import numpy as np
import json
import os
import os.path
from utilities import *
from scipy import spatial


d_segmentid_to_embedding = get_clipid_to_embedding_dict(dicts_dir="dicts-final-4d")
# print(sorted(d_segmentid_to_embedding.keys()))
# exit()
d_attr_to_clipids = get_attribute_to_clipids_dict(dicts_dir="dicts-final-4d")

d_clipid_to_attrs = {}
for attribute, clipids in d_attr_to_clipids.items():
	for clipid in clipids:
		if clipid not in d_clipid_to_attrs:
			d_clipid_to_attrs[clipid] = [attribute]
		else:
			d_clipid_to_attrs[clipid].append(attribute)
# print(sorted(d_clipid_to_attrs.keys()))
# exit()
d_segmentid_to_clipid = {}
for segmentid in d_segmentid_to_embedding.keys():
	d_segmentid_to_clipid[segmentid] = segmentid[:-3]

d_segmentid_to_attributes = {}
allowed_attributes = ["Distorted", "Bright", "Aggressive"]
for segmentid, clipid in d_segmentid_to_clipid.items():
	print(segmentid, clipid)
	if clipid in d_clipid_to_attrs:
		attrs = set(d_clipid_to_attrs[clipid]).intersection(allowed_attributes)
		if len(attrs) == 0:
			continue
		d_segmentid_to_attributes[segmentid] = ", ".join(attrs)



### The same embeddings as tsv files
with open(os.path.join("tsv-final-4d", "202203-attr-embeddings.tsv"), 'w', newline='') as f_output:
    f_output.seek(0)
    f_output.truncate()
    for segmentid in d_segmentid_to_attributes.keys():
        f_output.write("\t".join(str(x) for x in d_segmentid_to_embedding[segmentid]))
        f_output.write('\n')

with open(os.path.join("tsv-final-4d", "202203-attr-embeddings-names.tsv"), 'a') as f_output:
    f_output.seek(0)
    f_output.truncate()
    for attributes in d_segmentid_to_attributes.values():
        f_output.write(attributes)
        f_output.write('\n')

# print(d_segmentid_to_embedding)