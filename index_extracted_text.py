#import pysolr


'''
def index_document_with_vector(text, vector_filename, core_name, document_count):
    SOLR_ADDRESS = 'http://localhost:8983/solr/' + core_name
    solr = pysolr.Solr(SOLR_ADDRESS, always_commit=True)

    with open(vector_filename, "r") as vectors_file:
        vector_strings = vectors_file.readlines()
        
    #vector_dimension = 384  # Dimension based on your schema's "knn_vector" field type

    vectors = [[float(w) for w in vector_string.split(",")] for vector_string in vector_strings]

    #if len(vectors[0]) != vector_dimension:
    #    raise ValueError("Vector dimensions do not match the schema's 'knn_vector' field type")
    doc = {
        "id": str(document_count),  # Generate a unique ID
        "text": text,
        "vector": vectors
    }
    solr.add(doc)
    solr.commit()
    print("Indexed document with vectors")'''






