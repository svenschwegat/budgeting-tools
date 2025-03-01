from datetime import datetime
import json
import re

def init():
    config = get_config()
    categories = get_categories(config)
    year_month_input = input('What year and month (YY-MM):')

    input_file_path = get_input_file_path(config)
    json_list = parse_csv(config, categories, year_month_input, input_file_path)
    write_to_file(config, year_month_input, json_list)

def get_config():
    # config.json contains file paths and key words, see config_template
    with open('config.json', 'r', encoding = 'utf-8') as file:
        config = json.load(file)

    return config

def get_categories(config):
    # categories.json contains mapping of keywords to categories, see categories_template
    categories_file_path = config[0]['categories']['file_path'] + '\\' + config[0]['categories']['file_name']
    
    with open(categories_file_path, 'r', encoding = 'utf-8') as file:
        categories = json.load(file)
    
    return categories

def get_input_file_path(config):
    input_file_name = config[0]['input_csv']['file_name']
    input_file_path = config[0]['input_csv']['file_path'] + '\\' + input_file_name
     
    return input_file_path

def parse_csv(config, categories, year_month_input, input_file_path):
    input_pattern = r'(\d{2})-(\d{2})'
    match_input = re.match(input_pattern, year_month_input)
    requested_year = match_input.group(1)
    requested_month = match_input.group(2)

    with open(input_file_path, 'r', encoding = 'utf-8') as file:
        lines = file.readlines()

    delimiter = config[1]['csv']['delimiter']
    json_list = []
    category_not_found = 0
    date_pattern = r'^\d{2}\.(\d{2})\.(\d{2})'
    avoid_key_word = config[1]['csv']['avoid_key_word']

    for line in lines:
        item = line.split(delimiter)
        date = item[0].replace('"', '')
        found_date = re.search(date_pattern, date)  
        match_date = re.match(date_pattern, date)
        if found_date == None and match_date == None:
            continue
        match_date_year = match_date.group(2)
        match_date_month = match_date.group(1)

        if found_date and len(item) == 12 \
        and requested_year == match_date_year \
        and requested_month == match_date_month:
            name = item[4].strip().replace('"', '')
            purpose = item[5].strip().replace('"', '')
            amount = float(item[8].replace('.', '').replace(',', '.').replace('"', ''))

            if avoid_key_word in purpose:
                continue

            # Extract date
            date_match = re.search(date_pattern, date)
            if date_match:
                raw_date = date_match.group()
                date = datetime.strptime(raw_date, '%d.%m.%y').strftime('%Y-%m-%d')
            else:
                date = None
                print('Date not found @ ' + item)

            category, category_not_found = get_category(categories, category_not_found, name, purpose, amount)

            json_item = {
                    "date": date,
                    "name": name,
                    "purpose": purpose,
                    "amount": amount,
                    "category": category
                }
            json_list.append(json_item)

    if category_not_found > 0:
        print('Categories not found:', category_not_found, 'out of', len(json_list))
    else: 
        print('All categories found for', len(json_list), 'items')
    return json_list

def get_category(categories, category_not_found, name, purpose, amount):
    for i in categories:
        if any(keywords.lower() in purpose.lower() for keywords in i['mapping']):
            category = i['sub_category']
            break
        elif any(keywords.lower() in name.lower() for keywords in i['mapping']):
            category = i['sub_category']
            break
        elif amount >= 0:
            category = categories[3]['sub_category']
            break
        else:
            category = categories[-1]['sub_category']

    if category == categories[-1]['sub_category']:
        category_not_found += 1
        
    return category, category_not_found

def write_to_file(config, year_month_input, json_list):
    csv_key_word = config[1]['csv']['key_word']
    output_file_name = '20' + year_month_input + '-output-' + csv_key_word + '.json'
    output_file_path = config[0]['output']['file_path'] + '\\' + output_file_name
    with open(output_file_path, 'w') as file:
        json.dump(json_list, file, indent = 4)

    print('Output file created @', output_file_path)

init()