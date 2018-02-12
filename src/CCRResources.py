import os 

resources = {}

def populate(res_directory):
    for file in os.listdir(res_directory):
        resources[file] = os.path.join(res_directory,file)

def res(file_name):
    return resources[file_name]