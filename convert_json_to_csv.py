import pandas as pd
import json
import re

def init():
    config = get_config()
    file_paths = get_file_paths(config)
    merged_json = merge_json_files(file_paths)
    convert_json_to_csv(config, merged_json)

def get_config():
    # config.json contains file paths and key words, see config_template
    with open('config.json', 'r', encoding = 'utf-8') as file:
        config = json.load(file)

    return config

def get_file_paths(config):
    file_path = config[0]['output']['file_path']
    full_file_path = file_path + '\\' + config[0]['output']['file_name']
    full_file_path_2 = file_path + '\\' + config[0]['output']['file_name_2']
     
    return [full_file_path, full_file_path_2]

def merge_json_files(file_paths):
    merged_json = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding = 'utf-8') as file:
            json_list = json.load(file)
            merged_json.extend(json_list)

    return merged_json

def convert_json_to_csv(config, merged_json):
    filename = config[0]['output']['file_name']
    pattern = r'\d{4}\-\d{2}'
    match = re.match(pattern, filename)
    year_month = match.group(0)
    output_file_path = config[0]['output']['file_path'] + '\\' + year_month +  '-output-csv.csv'

    df = pd.DataFrame(merged_json)
    df.to_csv(output_file_path, index = False)

    print(f'File saved at {output_file_path} with {len(merged_json)} rows')

init()