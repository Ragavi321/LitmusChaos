import os

def read_config_file():
    env = os.environ['Environment']
    project = os.environ['Project']
    json_config_path = os.path.join(sys.path[0], project + "/" + "config_" + env + ".json")
    return json_config_path

def load_config_file():
    config_file_name = read_config_file()
    file = open(config_file_name)
    config_data = json.load(file)
    return config_data