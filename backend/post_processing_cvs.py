from query_solr import query_user_prompt, get_cv_chunks, get_cv_scores
import requests
import math
import pysolr

# function to get the top ranked cvs based on the calculated total score ...

def get_top_ranked_cvs(prompt,percentage_of_cvs):
    search_result=query_user_prompt(prompt)
    cv_scores=get_cv_scores(search_result)
    
    cv_chunks=get_cv_chunks(search_result)
    sorted_items = sorted(cv_scores.items(), key=lambda item: item[1], reverse=True)
    
    num_items = len(sorted_items)
    num_selected = int(num_items * percentage_of_cvs)
    rounded_num_selected = math.ceil(num_selected)
    top_items = sorted_items[:num_selected]
    top_keys = [item[0] for item in top_items]
    keep_only_selected_keys(cv_chunks,top_keys)

    print(cv_chunks)
    cv_documents= fetch_documents_by_cv_numbers(cv_chunks,'software_engineer')
    if cv_documents:
        print("Retrieved CV documents:")
        for cv_number, docs in cv_documents.items():
            print(f"CV Number: {cv_number}")
            for doc in docs:
                print(f"  ID: {doc['id']}, Text: {doc.get('text', 'N/A')}")
    
    return dict(top_items)


def keep_only_selected_keys(dictionary, keys_to_keep):
    keys_to_delete = [key for key in dictionary if key not in keys_to_keep]
    
    for key in keys_to_delete:
        del dictionary[key]

# query to retrieve the matching chunks in the accepted cvs
import requests

def fetch_documents_by_cv_numbers(cv_info_dict,core_name):

    solr_url = "http://localhost:8983/solr/" + core_name 
    # Extract the document IDs from the dictionary values
    ids = [doc_id for doc_ids in cv_info_dict.values() for doc_id in doc_ids]
    query = f"id:({' OR '.join(ids)})"
    params = {
        "q": query,
        "fl": "id,text",  # Specify the fields you want to retrieve
        "rows": len(ids)  # Number of rows to retrieve (equal to the number of IDs)
    }

    response = requests.get(f"{solr_url}/select", params=params)
    
    if response.status_code == 200:
        results = response.json()
        retrieved_documents = results['response']['docs']
        
        # Create a new dictionary with CV numbers as keys and documents as values
        cv_documents = {}
        for cv_number, doc_ids in cv_info_dict.items():
            cv_documents[cv_number] = []
            for doc_id in doc_ids:
                doc = next((d for d in retrieved_documents if d['id'] == doc_id), None)
                if doc:
                    cv_documents[cv_number].append({"id": doc['id'], "text": doc.get('text', 'N/A')})
                else:
                    print(f"Document with ID {doc_id} not found.")
        
        return cv_documents
    else:
        print(f"Solr request failed with status code: {response.status_code}")
        return None

if __name__== '__main__':
    
    selected_items = get_top_ranked_cvs('Find candidates with good analytical skills and are experienced in python',0.5)

    print("Selected items:")
    for item, value in selected_items.items():
        print(f"{item}: {value}")