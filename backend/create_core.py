import pysolr
import os
import requests

core_name=''

def create_cores(core_name):
    solr_base_url = "http://localhost:8983/solr"
    config_set_path = "E:\ITworx\Solr\solr-9.3.0\server\solr\my_configsets"  # Replace with your config set directory path
    schema_name= "E:\ITworx\Solr\solr-9.3.0\server\solr\my_configsets\schema.xml" # replace with your schema directory path
    create_core_url = f"{solr_base_url}/admin/cores"
    data = {
        "action": "CREATE",
        "name": core_name,
        "instanceDir": core_name,
        "configSet": config_set_path,
        "schema": schema_name
    }

    response = requests.post(create_core_url, data=data)
    print(response.text)
    return core_name


def create_folder_for_core(core_name):
    # Specify the path of the directory you want to create
    directory_path = "E:\ITworx\CVs\Documents"+ "\\" +core_name

    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully!")
    else:
        print(f"Directory '{directory_path}' already exists.")
    return directory_path

def delete_documents_in_core(core_name):
    solr = pysolr.Solr('http://localhost:8983/solr/'+ core_name)
    solr.delete(q='*:*')
    solr.commit()

if __name__ == "__main__":
    pass
    #create_cores('software_engineer')
    #core_name= create_cores('software_engineer')
    #create_folder_for_core(core_name)
    delete_documents_in_core('software_engineer')