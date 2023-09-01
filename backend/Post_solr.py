from urllib.request import urlopen
from backend.embeddings import batch_encode_to_vectors
from index_documents import index_documents, index_extracted_documents
from extract_text import extract_text_from_pdf, preprocess_text_modified
import os
import csv
import pysolr
from tika import parser

def get_documents_in_folder(folder_path):

    #folder_path = 'E:\ITworx\CVs\Documents'  # replace with the path to your folder
    file_list = os.listdir(folder_path)
    id_number=100
    cv_name = 'CV'
    counter =0
    
    for file_name in file_list:
        
        if file_name.endswith('.pdf'):  # replace '.txt' with the file extension you want to read
            counter+=1
            cv_name += str(counter)
            
            file_path = os.path.join(folder_path, file_name)
            
            core_name= os.path.basename(folder_path)
            core_name_no_extenstion= os.path.splitext(core_name)[0]

            basename = os.path.basename(file_name)
            name_without_extension = os.path.splitext(basename)[0]

            name_for_csv = name_without_extension +'.csv'

            csv_file_path= create_csv(core_name_no_extenstion,name_for_csv)

            # extract the text from pdf
            extracted_text= extract_text_from_pdf(file_path)

            # remove extra spaces and preprocess the extracted text
            prepocessed_text= preprocess_text_modified(extracted_text)
            # create text file to store the extracted text
            name_for_text = name_without_extension + '.txt'
            txt_file_path=save_text_to_file(prepocessed_text,name_for_text,folder_path) # pass the text, name for the text file, and the folder path of the to be created file
            
            # encode extracted text using word2vec which takes as input the extracted text it self and not the text file
            #create_word2vec_model(prepocessed_text,csv_file_path)

            # call def batch_encode_to_vectors

            batch_encode_to_vectors(txt_file_path,csv_file_path)

            # index the extracted text to solr
            index_documents(txt_file_path,csv_file_path,core_name,cv_name)
            cv_name = 'CV'

def create_dictionary(cv_name,cv_scores):
    cv_scores[cv_name] = 0
    return cv_scores
    

def save_text_to_file(text_lines, output_filename, directory):
    file_path = os.path.join(directory, output_filename)
    with open(file_path, "w", encoding="utf-8") as file:
        for line in text_lines:
            # Write each line of text as a separate line in the file
            file.write(line + '\n')
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