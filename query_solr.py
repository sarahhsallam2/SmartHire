import requests
import json
from embeddings import get_sentence_embedding
import re
from collections import Counter
from Post_solr import create_dictionary

def search_with_sentence_embedding(embedding_vector,core_name, k=20):
    solr_url = "http://localhost:8983/solr/" + core_name 
    if len(embedding_vector) != 384:
        print(f"Error: The provided vector has dimension {len(embedding_vector)}, but {384} is expected.")
        return None
    
    solr_query = {
        "query": f"{{!knn f=vector topK={k}}}[{', '.join(map(str, embedding_vector))}]"
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{solr_url}/select?fl=id,text,score", data=json.dumps(solr_query), headers=headers)

    if response.status_code == 200:
        results = response.json()
        return results
    else:
        print(f"Solr request failed with status code: {response.status_code}")
        print(response.text)
        return None


def query_user_prompt(prompt):

    sentence_vector=get_sentence_embedding(prompt)
    #search(sentence_vector)
    search_results = search_with_sentence_embedding(sentence_vector,'software_engineer')

    return search_results

def get_cv_scores(search_results):
    if search_results:
        #print("Search results in scores:")
        cv_scores ={}
       
        for doc in search_results['response']['docs']:
            output_string = re.sub(r'_.*', '', doc['id']) # CV1
            
            if output_string in cv_scores:
                cv_scores[output_string] += doc['score']
            else: 
                cv_scores[output_string]= doc['score']
            #print(f"ID: {doc['id']}, Text: {doc['text']}, Score: {doc['score']}")
    return cv_scores

def get_cv_chunks(search_results):
    if search_results:
        #print("Search results in chunks:")
        cv_chunks={}
        for doc in search_results['response']['docs']:
            output_string = re.sub(r'_.*', '', doc['id']) # CV1
            
            if output_string in cv_chunks:
                cv_chunks[output_string].append(doc['id'])
            else: 
                cv_chunks[output_string] =[]
                cv_chunks[output_string].append(doc['id'])
            #print(f"ID: {doc['id']}, Text: {doc['text']}, Score: {doc['score']}")
    return cv_chunks

if __name__== '__main__':
    query_user_prompt('Find candidates with good analytical skills and are experienced in python')
    
        
