import words
import os
from gensim.models import KeyedVectors
vecs = KeyedVectors.load_word2vec_format('/Users/pratik/My Drive/utokyo/08. research/GoogleNews-vectors-negative300.bin', binary=True, limit=10000000)

with open(os.path.join("embeddings.tsv"), 'a') as f_embeddings, open("words.tsv", 'a') as f_words:
    f_embeddings.seek(0)
    f_embeddings.truncate()
    f_words.seek(0)
    f_words.truncate()
    for w in words.words:
    	if w.lower() in vecs:
    		vec = list(vecs[w.lower()])
    		f_embeddings.write("\t".join(str(v) for v in vec))
    		f_words.write(w)
	    	f_embeddings.write('\n')
    		f_words.write('\n')
    	else:
    		print(w, " not found!!")


