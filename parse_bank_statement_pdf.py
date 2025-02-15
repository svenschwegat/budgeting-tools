from PyPDF2 import PdfReader
from datetime import datetime
import re
import json

def init():
    input_file_path = read_files()
    items = extract_text(input_file_path)
    json_list = create_json(items)
    write_to_file(json_list)

    if category_not_found > 0:
        print('Categories not found:', category_not_found, 'out of', len(json_list))
    else: 
        print('All categories found for', len(json_list), 'items')
    
def read_files():
    # config.json contains file paths and key words, see config_template
    with open('config.json', 'r', encoding = 'utf-8') as file:
        global config
        config = json.load(file)

    categories_file_path = config[0]['categories']['file_path'] + '\\' + config[0]['categories']['file_name']

    # categories.json contains mapping of keywords to categories, see categories_template
    with open(categories_file_path, 'r', encoding = 'utf-8') as file:
        global global_mapping_categories
        global_mapping_categories = json.load(file)
    
    global input_file_name
    input_file_name = config[0]['input']['file_name']
    input_file_path = config[0]['input']['file_path'] + '\\' + input_file_name    
    
    global category_not_found
    category_not_found = 0
     
    return input_file_path

def extract_text(file_path):
    reader = PdfReader(file_path)
    number_of_pages = len(reader.pages)
    items = []

    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()

        if i == 0: # first page
            page_type = 'first_page' 
        elif i == number_of_pages - 1: # last page
            page_type = 'last_page'
        else: # all other pages
            page_type = 'middle_page'

        begin_key_word = config[1][page_type]['begin_key_word']
        end_key_word = config[1][page_type]['end_key_word']

        item = get_relevant_content(text, begin_key_word, end_key_word)
        items.extend(item)

    return items

def get_relevant_content(text, begin_key_word, end_key_word):
    beginning = text.find(begin_key_word)
    end = text.find(end_key_word)
    
    if beginning == end:
        end = text.find(end_key_word, end + len(end_key_word))

    data = text[beginning:end]

    pattern = r'\d{2}\.\d{2}\.\d{4}'
    item = re.split(f'(?={pattern})', data)
    return item

def create_json(items):
    json_list = []
    name = 'Kartenumsatz'
    for item in items:
        if name in item:
            # Extract date
            date_pattern = r'\d{2}\.\d{2}\.\d{4}'
            date_match = re.search(date_pattern, item)
            if date_match:
                raw_date = date_match.group()
                date = datetime.strptime(raw_date, '%d.%m.%Y').strftime('%Y-%m-%d')
            else:
                date = None
                print('Date not found @ ' + item)
                
            # Extract purpose and amount
            purpose_amount_pattern = name + r'\n(.*?),\s*(.*?)\s*(-?\d+,\d{2})'
            purpose_amount_match = re.search(purpose_amount_pattern, item, re.DOTALL)

            if purpose_amount_match:
                purpose = purpose_amount_match.group(1).strip()
                amount = float(purpose_amount_match.group(3).replace(',', '.'))
                category = get_category(purpose)

                json_item = {
                    "date": date,
                    "name": name,
                    "purpose": purpose,
                    "amount": amount,
                    "category": category
                }
                json_list.append(json_item)
            else:
                print('Purpose and amount not found @ ' + item)
    
    return json_list

def get_category(purpose):
    categories = global_mapping_categories
    global category_not_found

    for i in categories:
        if any(keywords.lower() in purpose.lower() for keywords in i['mapping']):
            category = i['sub_category']
            break
        else:
            category = categories[-1]['sub_category']

    if category == categories[-1]['sub_category']:
        category_not_found += 1
    return category

def write_to_file(json_list):
    # Extract current year and month and write to file
    key_word = config[0]['input']['key_word']
    pattern = '(?:' + key_word + r'-)(\d{2}\-\d{2})' 
    match = re.search(pattern, input_file_name)
    if match:
        output_file_name = match.group(1) + '-output-' + key_word + '.json'
    else:
        output_file_name = 'failed_naming_output.json'

    output_file_path = config[0]['output']['file_path'] + '\\' + output_file_name
    with open(output_file_path, 'w') as file:
        json.dump(json_list, file, indent = 4)

    print('Output file created @', output_file_path)

init()