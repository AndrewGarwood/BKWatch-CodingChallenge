import re
import argparse
import csv
import xml.etree.ElementTree as ET
import json
import ast
from typing import List, Dict

# TODO: you know the thing
#       Add error handling for invalid file formats
#       make sure can handle input w/ entire filepaths, not just file name
#       clean up everything

# PEP **8** Style Guide Notes:
# Limit all lines to a maximum of 79 characters.
# docstrings or comments limit to 72 characters.
# 4 space indentation
tsv_columns = ['name', 'organization', 'street', 'city', 'state', 'county',
               'zip'
]
xml_keys = ['name', 'organization', 'street', 'city', 'state', 'zip']
xml_elements = ['NAME', 'COMPANY', 'STREET', 'CITY', 'STATE', 'POSTAL_CODE']
xml_address = ['STREET', 'STREET_2', 'STREET_3']

def parse_xml(filepath: str, xml_data: List) -> List:
    with open(filepath, 'r') as file:
        tree = ET.parse(file)
        root = tree.getroot()
        ent_list = root.findall(path='ENTITY/ENT')
        for ent in ent_list:
            xml_data.append(get_ent_data(ent, {}))
    return xml_data

def parse_tsv(filepath: str, tsv_data: List) -> List:
    with open(filepath, 'r') as file:
        tsv_reader = csv.reader(file, delimiter="\t")   
        next(tsv_reader)  # skip tsv_columns row
        for row in tsv_reader:  # row is list w/ len=10  
            if (row is not None and row):  
                row_data = {}
                row_name, is_org = get_name(row)
                if is_org: row_data['organization'] = row_name
                else: row_data['name'] = row_name
                for key, value in zip(tsv_columns[2:6], row[4:8]):
                    if (value and value != 'N/A'):
                        row_data[key] = value     
                row_data['zip'] = get_zip(zip=row[8], zip4=row[9])
                tsv_data.append(row_data)
            
        return tsv_data # list of JSON objects

def parse_txt(filepath: str, txt_data: List) -> List:
    with open(filepath, 'r') as file:
        file_data = file.read().strip()  
        address_pattern = (
            r'(?P<name>.+)\n'
            r'(?P<street>.+)\n'
            r'(?:\n?(?P<county>[A-Z\s]+) COUNTY\n)?'
            r'(?P<city>[^\d\n]+),\s*(?P<state>[A-Za-z]+),?\s*'
            r'(?P<zip>\d{5}(?:-\d{4})?)'
        )  # multi-line string literal :o
        match_list = list(re.finditer(address_pattern, file_data))
        for match in match_list:
            address_dict = match.groupdict()
            for key in address_dict.keys():
                if (key and address_dict[key]):
                    address_dict[key] = address_dict[key].strip()
            if address_dict.get('county') is None:
                del address_dict['county']
            txt_data.append(address_dict)     
        return txt_data

def get_ent_data(ent: ET.Element, data: Dict) -> Dict:
    for key, element in zip(xml_keys, xml_elements):
        value = ent.findtext(element).strip(' -')
        if element == 'STREET':       
            data['street'] = ' '.join([f'{ent.findtext(line)}'
                                       for line in xml_address]
            ).strip()
            pass
        elif element == 'POSTAL_CODE':
            data['zip'] = value.replace(' ', '')
        elif value:  #len(value) > 0:
            data[key] = value
    return data

def get_name(row: List):
    first, middle, last, org = row[0], row[1], row[2], row[3]
    name, is_org = '', False
    # assuming existence of first+last always corresponds to a person
    if first and last:
        if middle != 'N/M/N':
            name = f'{first} {middle} {last}'
        else:
            name = f'{first} {last}'
    elif org and org != 'N/A':
        is_org = True
        name = org
    elif last and org == 'N/A':  # if org and last name data mismatched
        is_org = True
        name = last
    return name, is_org

def get_zip(zip: str, zip4: str) -> str:
    if zip4:
        return f'{zip}-{zip4}'
    else:
        return zip

def sorted_data(data: List[Dict]):
    return sorted(data, key=sorting_key) 

def extract_zip(address: Dict):
    zip_code = address.get('zip')  
    return zip_code.replace('-', '')  

def sorting_key(address: Dict):
    return extract_zip(address)

def get_filedata_from_paths(path_list: List, sort_data: bool):
    xml_data, tsv_data, txt_data, all_data = [], [], [], []
    for p in path_list:
        ext = p[-3:].lower()  # assuming len(file extension) = 3; add check for valid file type
        if ext == "xml":
            xml_data = parse_xml(filepath=p, xml_data=xml_data)
        elif ext == "tsv":
            tsv_data = parse_tsv(filepath=p, tsv_data=tsv_data)
        elif ext == "txt":
            txt_data = parse_txt(filepath=p, txt_data=txt_data)
    all_data.extend(xml_data)
    all_data.extend(tsv_data)
    all_data.extend(txt_data)
    if sort_data:
        all_data = sorted_data(all_data)
    return all_data

def validate_file_extensions(paths: List[str]):
    return paths

def parse_paths(input_str: str) -> List[str]:
    try:  # check if input string is in list format
        paths = ast.literal_eval(input_str)
        if not isinstance(paths, list):
            raise ValueError
        paths_with_brackets = ast.literal_eval('['+input_str+']', list)
        if not isinstance(paths_with_brackets, list):
            raise ValueError
    except (SyntaxError, ValueError):  # else split the string manually
        pattern = r'(?<=\.(?:xml|tsv|txt)),?\s*(?=\w)'  # TODO document this
        paths = re.split(pattern, input_str) 
    # Strip extraneous characters that the user may have typed
    # use set comprehension so don't end up w/ duplicate filepaths
    paths = list({p.strip("', []") for p in paths if p.strip()})
    # paths = validate_file_extensions(paths)
    return paths

if __name__ == "__main__":
    # main()
    parser = argparse.ArgumentParser(description='Process files from paths.')
    # parser.add_argument('--help', action='help', help='Show this help message and exit')
    input_str = input("Please enter a list of path(s): ")
    paths = parse_paths(input_str)
    # validate_file_extensions(paths)
    filedata = get_filedata_from_paths(path_list=paths, sort_data=True)
    print(json.dumps(filedata, indent=2))


# TODO:
# * Provide a `--help` option
# * Check for errors in the argument list
# * Check the input files to make sure they conform to the formats exemplified by the sample files 
# * Output a list of addresses only if no errors were discovered in the above two steps
# * Write any error messages to stderr
# * Exit with status `0` or `1` to indicate success or failure