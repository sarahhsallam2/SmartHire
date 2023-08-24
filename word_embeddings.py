from gensim.models import Word2Vec
import numpy as np
import sys

def create_word2vec_model(text, output_filename):
    # Split the text into segments based on spaces
    segments = text.split()  # Split by spaces

    model = Word2Vec(sentences=[segments], vector_size=384, window=5, min_count=1, sg=0)

    with open(output_filename, 'w+', newline='') as out:
        for word in model.wv.index_to_key:
            vector=model.wv[word]
            normalized_vector = vector / np.linalg.norm(vector)
            vector_str = ",".join([str(i) for i in normalized_vector])
            out.write(vector_str)
            out.write('\n')
        
    '''with open(output_filename, 'w+') as out:
        for word in model.wv.index_to_key:
            vector = model.wv[word]
            normalized_vector = vector / np.linalg.norm(vector)
            vector_str = ",".join([str(i) for i in normalized_vector])
            out.write(vector_str)
            out.write('\n')'''
    '''segments = text.split()  # Split by spaces
    
    model = Word2Vec(sentences=[segments], vector_size=100, window=5, min_count=1, sg=0)

    with open(output_filename, 'w+') as out:
        for word in model.wv.index_to_key:
            vector = model.wv[word]
            normalized_vector = vector / np.linalg.norm(vector)
            vector_str = ",".join([str(i) for i in vector])
            out.write(vector_str)
            out.write('\n')'''


    

