import sys
import pysolr



def index_documents(documents_filename, embedding_filename,core_name):
        ## Solr configuration.
    SOLR_ADDRESS = 'http://localhost:8983/solr/'+ core_name
    # Create a client instance.
    solr = pysolr.Solr(SOLR_ADDRESS, always_commit=True)

    BATCH_SIZE = 100
    # Open the file containing text.
    with open(documents_filename, "r") as documents_file:
        # Open the file containing vectors.
        with open(embedding_filename, "r") as vectors_file:
            documents = []
            # For each document creates a JSON document including both text and related vector. 
            for index, (document, vector_string) in enumerate(zip(documents_file, vectors_file)):

                vector = [float(w) for w in vector_string.split(",")]
                doc = {
                    "id": str(index),
                    "text": document,
                    "vector": vector
                }
                # Append JSON document to a list.
                documents.append(doc)

                # To index batches of documents at a time.
                if index % BATCH_SIZE == 0 and index != 0:
                    # How you'd index data to Solr.
                    solr.add(documents)
                    documents = []
                    print("==== indexed {} documents ======"
                    .format(index))
        # To index the rest, when 'documents' list < BATCH_SIZE.
            if documents:
                solr.add(documents)
            print("finished")

def main():
    document_filename = sys.argv[1]
    embedding_filename = sys.argv[2]
    index_documents(document_filename, embedding_filename)

if __name__ == "__main__":
    main()