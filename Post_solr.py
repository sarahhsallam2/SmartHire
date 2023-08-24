from urllib.request import urlopen
from create_core import core_name
#from embeddings import batch_encode_to_vectors
from index_documents import index_documents, index_extracted_documents
from extract_text import extract_text_from_pdf, preprocess_text
from word_embeddings import create_word2vec_model
#from index_extracted_text import index_document_with_vector
import os
import csv
import pysolr
from tika import parser

def push_to_solr(file_path,id_number):
    
    solr = pysolr.Solr('http://localhost:8983/solr/software_tester', always_commit=True)

    pdf_file_path = file_path
    #pdf_file_name = os.path.basename(pdf_file_path)
    parsed_pdf = parser.from_file(pdf_file_path)
    pdf_content = parsed_pdf['content']
    doc = {'id': id_number, 'content': pdf_content} # id will be passed as a parameter to increment continously

    solr.add([doc])

def get_documents_in_folder(folder_path):

    #folder_path = 'E:\ITworx\CVs\Documents'  # replace with the path to your folder
    file_list = os.listdir(folder_path)
    id_number=100
    for file_name in file_list:
        if file_name.endswith('.pdf'):  # replace '.txt' with the file extension you want to read
            file_path = os.path.join(folder_path, file_name)
            
            core_name= os.path.basename(folder_path)
            core_name_no_extenstion= os.path.splitext(core_name)[0]

            basename = os.path.basename(file_name)
            name_without_extension = os.path.splitext(basename)[0]

            name_for_csv = name_without_extension +'.csv'
            #core_name='software_tester'
            csv_file_path= create_csv(core_name_no_extenstion,name_for_csv)

            # extract the text from pdf
            extracted_text= extract_text_from_pdf(file_path)

            # remove extra spaces and preprocess the extracted text
            prepocessed_text= preprocess_text(extracted_text)
            # create text file to store the extracted text
            name_for_text = name_without_extension + '.txt'
            txt_file_path=save_text_to_file(prepocessed_text,name_for_text,folder_path) # pass the text, name for the text file, and the folder path of the to be created file
            
            # encode extracted text using word2vec which takes as input the extracted text it self and not the text file
            create_word2vec_model(prepocessed_text,csv_file_path)

            # call def batch_encode_to_vectors
            #batch_encode_to_vectors(file_path,csv_file_path)

            # index the extracted text to solr
            index_documents(txt_file_path,csv_file_path,core_name,id_number)
            #index_extracted_documents(prepocessed_text,csv_file_path,core_name_no_extenstion) # function that will take the extracted text immediately and index it afterwards didn't work
            id_number+=1

def save_text_to_file(text, output_filename,directory):
    file_path = os.path.join(directory, output_filename)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
    return file_path

def create_csv(core_name,file_name):
    directory = 'E:\ITworx\CVs\Documents'+"\\" + core_name
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, file_name)

    with open(os.path.join(directory, file_name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([])  
    return filepath     
       
if __name__ == "__main__":
    # replace with the file directory for the generated core
    get_documents_in_folder('E:\ITworx\CVs\Documents\software_engineer')   