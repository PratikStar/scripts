import os, csv, json
import os.path

def save_as_dict(d, path):
    json.dump(d, open(path,'w'))

def get_as_dict(path):
    with open(path) as f:
        data = f.read()
            
    d = json.loads(data)
    return d

# gets from the file if the file exists Or calculates from dynamo/drive export
def get_attribute_to_clipids_dict(dicts_dir="dicts", exports_dynamo_directory = "../exports-dynamo"):
    
    path = os.path.join(dicts_dir, "dict_attribute_to_clipids.txt")
    if os.path.isfile(path):
        print("File found: attr -> clipid")
        return get_as_dict(path)

    return calculate_attribute_to_clipids_dict(exports_dynamo_directory)

def calculate_attribute_to_clipids_dict(exports_dynamo_directory = "../exports-dynamo"):
    d = {}
    with open(os.path.join(exports_dynamo_directory, '20210905160610-timbre_survey.csv'), 'r', newline='')  as f:
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

# gets from the file if the file exists Or calculates from dynamo/drive export
def get_clipid_to_embedding_dict(dicts_dir="dicts", exports_drive_directory = "../exports-drive", embeddingfn = "embeddings.tsv", embeddingfnfn="embedding-filenames.tsv"):
    
    path = os.path.join(dicts_dir, "dict_clipid_to_embedding.txt")
    if os.path.isfile(path):
        print("File found: id -> embedding")
        return get_as_dict(path)

    return calculate_clipid_to_embedding_dict(exports_drive_directory, embeddingfn, embeddingfnfn)


def calculate_clipid_to_embedding_dict(exports_drive_directory = "../exports-drive", embeddingfn = "embeddings.tsv", embeddingfnfn="embedding-filenames.tsv"):
    filenames = []
    with open(os.path.join(exports_drive_directory, embeddingfnfn), 'r') as f:
        r = csv.reader(f, delimiter='\t')
        for row in r:
            filenames.append(row[0])
            # print(row)
    vec = []
    with open(os.path.join(exports_drive_directory, embeddingfn), 'r') as f:
        r = csv.reader(f, delimiter='\t')
        for row in r:
            float_row = [float(i) for i in row]
            vec.append(float_row)
            # print(row)

    d_name_vec = {}
    for i in range(0, len(filenames)):
        d_name_vec[filenames[i].split(' ')[0]] = vec[i]

    return d_name_vec

# gets from the file if the file exists Or calculates from dynamo/drive export
def get_clipid_to_clipname_dict(exports_drive_directory = "../exports-drive"):
    
    path = os.path.join("dicts", "dict_clipid_to_clipname.txt")
    if os.path.isfile(path):
        return get_as_dict(path)

    return calculate_clipid_to_clipname_dict(exports_drive_directory)

def calculate_clipid_to_clipname_dict(exports_drive_directory = "../exports-drive"):
    filenames = []
    d = {}
    with open(os.path.join(exports_drive_directory, 'embedding-filenames.tsv'), 'r') as f:
        r = csv.reader(f, delimiter='\t')
        for row in r:
            short = row[0].split(' ')[0]
            d[short] = row[0]
    return d


# gets from the file if the file exists Or calculates from dynamo/drive export
def get_attribute_to_embeddings_dict(dicts_dir="dicts", exports_dynamo_directory = "../exports-dynamo", exports_drive_directory = "../exports-drive"):
    
    path = os.path.join(dicts_dir, "dict_attribute_to_embeddings.txt")
    if os.path.isfile(path):
        print("File found: attr -> embeddings")
        return get_as_dict(path)

    return calculate_attribute_to_embeddings_dict(exports_dynamo_directory)

def calculate_attribute_to_embeddings_dict(exports_dynamo_directory = "../exports-dynamo", exports_drive_directory = "../exports-drive"):
    d_attribute_to_clipids = calculate_attribute_to_clipids_dict(exports_dynamo_directory)
    d_clipid_to_embedding = calculate_clipid_to_embedding_dict(exports_drive_directory)

    d_attribute_to_embeddings = {}
    for k in d_attribute_to_clipids.keys():
        d_attribute_to_embeddings[k] = []
        clips = d_attribute_to_clipids[k]

        for clipid in clips:
            for windowed_clipid in d_clipid_to_embedding.keys():
                if clipid == windowed_clipid[0:8]:
                    d_attribute_to_embeddings[k].append(d_clipid_to_embedding[windowed_clipid])

    return d_attribute_to_embeddings
