import sqlite3
import json

def init():
    config = get_config()
    data = get_data(config)
    write_to_sqlite(config, data)

def get_config():
    # config.json contains file paths and key words, see config_template
    with open('config.json', 'r', encoding = 'utf-8') as file:
        config = json.load(file)

    return config

def get_data(config):
    file_path = config[0]['output']['file_path'] + '\\' + config[0]['output']['file_name'] 
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data

def write_to_sqlite(config, data):
    file_path = config[0]['sqlite']['file_path'] + '\\' + config[0]['sqlite']['file_name']
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    table_name = config[0]['sqlite']['table_name']
    row_names = config[0]['sqlite']['row_names']
    value_names = config[0]['sqlite']['value_names']

    counter = 0
    for row in data:
        cursor.execute(f"INSERT INTO {table_name} ({row_names}) VALUES ({value_names})", row)
        counter += 1

    conn.commit()
    conn.close()

    print(f"Data inserted successfully! Rows inserted: {counter}" )

init()