from urllib.request import urlopen
from embeddings import batch_encode_to_vectors
import os
import csv
import pysolr
from tika import parser

def push_to_solr(file_path,id_number):
    
    solr = pysolr.Solr('http://localhost:8983/solr/Resumes', always_commit=True)

    pdf_file_path = file_path
    #pdf_file_name = os.path.basename(pdf_file_path)
    parsed_pdf = parser.from_file(pdf_file_path)
    pdf_content = parsed_pdf['content']
    doc = {'id': id_number, 'content': pdf_content} # id will be passed as a parameter to increment continously

    solr.add([doc])

def get_documents_in_folder(folder_path):

    #folder_path = 'E:\ITworx\CVs\Documents'  # replace with the path to your folder
    file_list = os.listdir(folder_path)
    id_number=10
    for file_name in file_list:
        if file_name.endswith('.pdf'):  # replace '.txt' with the file extension you want to read
            file_path = os.path.join(folder_path, file_name)
            
            basename = os.path.basename(file_name)
            name_without_extension = os.path.splitext(basename)[0]

            name_without_extension+='.csv'
            csv_file_path= create_csv(name_without_extension)
            # call def batch_encode_to_vectors
            batch_encode_to_vectors(file_path,csv_file_path)
            #push_to_solr(file_path,id_number)
            id_number+=1
            #with open(file_path, 'r') as f:
            #   file_contents = f.read()

def create_csv(file_name):
    directory = 'E:\ITworx\CVs\Converted'
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, file_name)

    with open(os.path.join(directory, file_name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([])  
    return filepath     
       
if __name__ == "__main__":
    get_documents_in_folder()   
