import re
import ast
import csv
import xml.etree.ElementTree as ET
import json
from typing import List, Dict
from operator import methodcaller

# TODO: you know the thing
#       Add error handling for invalid file formats
#       clean up comments and docstrings and everything
#       b/c this unsightly

# PEP **8** Style Guide Notes:
# Limit all lines to a maximum of 79 characters.
# For(docstrings or comments), limit to 72 characters.
# 4 space indentation
tsv_columns = ['name', 'organization', 'street', 'city', 'state', 'county',
               'zip'
]
xml_keys = ['name', 'organization', 'street', 'city', 'state', 'zip']
xml_elements = ['NAME', 'COMPANY', 'STREET', 'CITY', 'STATE', 'POSTAL_CODE']
xml_address = ['STREET', 'STREET_2', 'STREET_3']

def parse_tsv(filepath: str, tsv_data: List) -> List:
    with open(filepath, 'r') as file:
        tsv_reader = csv.reader(file, delimiter="\t")   
        next(tsv_reader)  # skip tsv_columns row
        for row in tsv_reader:  # row is list w/ len=10    
            if (row is not None and len(row) > 0):
                row_data = {}
                row_name, is_org = get_name(row)
                if is_org: row_data['organization'] = row_name
                else: row_data['name'] = row_name
                for key, value in zip(tsv_columns[2:6], row[4:8]):  # this ain't clean
                    if (len(value) > 0 and value != 'N/A'):
                        row_data[key] = value     
            
                row_data['zip'] = get_zip(zip=row[8], zip4=row[9])
                tsv_data.append(row_data)
            # print(f'row_data:\n{json.dumps(row_data, sort_keys=False, indent=2)}')  
        return tsv_data # list of JSON objects

def parse_txt(filepath: str, txt_data: List) -> List:
    with open(filepath, 'r') as file:
        file_data = file.read().strip()
        # make pattern fit within col79
        address_pattern = r'(?P<name>.+)\n(?P<street>.+)\n(?:\n?(?P<county>[A-Z\s]+) COUNTY\n)?(?P<city>[^\d\n]+),\s*(?P<state>[A-Za-z]+),?\s*(?P<zip>\d{5}(?:-\d{4})?)'
        match_list = list(re.finditer(address_pattern, file_data))
        for match in match_list:
            address_dict = match.groupdict()
            for key in address_dict.keys():
                address_dict[key] = address_dict[key].strip()
            txt_data.append(address_dict)
        
        return txt_data
    
def parse_xml(filepath: str, xml_data: List) -> List:
    with open(filepath, 'r') as file:
        tree = ET.parse(file)
        root = tree.getroot()
        ent_list = root.findall(path='ENTITY/ENT')
        for ent in ent_list:
            xml_data.append(get_ent_data(ent, {}))
    return xml_data

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
        elif len(value) > 0:
            data[key] = value
    return data

def get_name(row: List):
    first, middle, last, org = row[0], row[1], row[2], row[3]
    name, is_org = '', False
    
    if first and last:  # assuming existence of first+last always corresponds to a person
        if middle != 'N/M/N':
            name = f'{first} {middle} {last}'
        else:
            name = f'{first} {last}'
    elif org and org != 'N/A':
        is_org = True
        name = org
    elif last and org == 'N/A':  # case when data is mismatched
        is_org = True
        name = last
    
    return name, is_org

def get_zip(zip: str, zip4: str) -> str:
    if zip4:
        return f'{zip}-{zip4}'
    else:
        return zip

def parse_paths(input_str: str) -> List:
    try:  # check if input string is in list format.. maybe also see if adding brackets to ends results in list
        paths = ast.literal_eval(input_str)
        if not isinstance(paths, list):
            raise ValueError
    except (SyntaxError, ValueError):  # else split the string manually
        pattern = r'(?<=\.(?:xml|tsv|txt)),?\s*(?=\w)'  # TODO document this
        paths = re.split(pattern, input_str) 
    # Strip extraneous characters that the user may have typed
    # make type(paths)=set so no duplicate files
    paths = [p.strip("', []") for p in paths if p.strip()]
    return paths

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

def sorted_data(data: List[Dict]):  # could add parameter to abstract/generalize for keys other than zip code
    return sorted(data, key=sorting_key) 

def extract_zip(address: Dict):
  zip_code = address.get('zip')  
  return zip_code.replace('-', '')  

def sorting_key(address: Dict):
  print(type(address))
  return extract_zip(address)

if __name__ == "__main__":
    input_str = input("Please enter a list of paths: ")
    paths = parse_paths(input_str)
    filedata = get_filedata_from_paths(path_list=paths, sort_data=True)
    print(json.dumps(filedata, indent=2))
