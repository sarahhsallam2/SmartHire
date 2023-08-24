'''from sentence_transformers import SentenceTransformer
import torch
import sys
from itertools import islice

BATCH_SIZE = 100
INFO_UPDATE_FACTOR = 1
MODEL_NAME = 'all-MiniLM-L6-v2'

# Load or create a SentenceTransformer model.
model = SentenceTransformer(MODEL_NAME)

# Get device like 'cuda'/'cpu' that should be used for computation.
if torch.cuda.is_available():
    model = model.to(torch.device("cuda"))
print(model.device)

def batch_encode_to_vectors(input_filename, output_filename):
    # Open the file containing text.
    with open(input_filename, 'r') as documents_file:
        # Open the file in which the vectors will be saved.
        with open(output_filename, 'w+') as out:
            processed = 0
            # Processing 100 documents at a time.
            for n_lines in iter(lambda: tuple(islice
            (documents_file, BATCH_SIZE)), ()):
                processed += 1
                if processed % INFO_UPDATE_FACTOR == 0:
                    print("processed {} batch of documents"
                    .format(processed))
                # Create sentence embedding
                vectors = encode(n_lines)
                # Write each vector into the output file.
                for v in vectors:
                    out.write(','.join([str(i) for i in v]))
                    out.write('\n')
                    

def encode(documents):
    embeddings = model.encode(documents, show_progress_bar=True)
    print('vector dimension: ' + str(len(embeddings[0])))
    return embeddings
'''