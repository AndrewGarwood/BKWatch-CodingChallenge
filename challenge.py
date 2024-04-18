import re
import ast
import csv
import xml.etree.ElementTree as ET
import json
from typing import List

# TODO: 
#       Add error handling for invalid file formats
#       clean up comments and docstrings
#       clean up everything for PEP 8 b/c this sh unsightly

# PEP **8** Style Guide Notes: (will delete this later)
# Limit all lines to a maximum of 79 characters.
# For(docstrings or comments), limit to 72 characters.
# 4 space indentation
tsv_headers = ['name', 'organization', 'street', 'city', 'state', 'county',
                 'zip']
def parse_tsv(filepath: str) -> List:
    result = []
    with open(filepath, 'r') as file:
        tsv_reader = csv.reader(file, delimiter="\t")   
        next(tsv_reader)  # skip the header row
        for row in tsv_reader:  # type(row) == list
            assert(row != [] and row != None)
            print(f'row: {row}')  # who doesn't love print statements?
            row_data = {}

            row_name, is_org = get_name(row)
            if is_org: row_data['organization'] = row_name
            else: row_data['name'] = row_name
            for key, value in zip(tsv_headers[2:6], row[4:8]):  # this ain't clean
                if value != '' and value != 'N/A':
                    row_data[key] = value     
        
            row_data['zip'] = handle_zip(zip=row[8], zip4=row[9])
            result.append(row_data)
            print(f'row_data:\n{json.dumps(row_data, sort_keys=False, indent=2)}')  
        return result # list of JSON objects

def parse_txt(filepath: str) -> List:
    return []  # list of JSON objects

def parse_xml(filepath: str) -> List:
    return []  # list of JSON objects

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
    
    return name, is_org  # type: ignore

def handle_zip(zip: str, zip4: str) -> str:
    if zip4 and zip4 != '':
        # could check len(zip4) == 4 and is soley digits
        return f'{zip}-{zip4}'
    else:  # zip4 == '':
        return zip


# could rename this to process_input or something more descriptive... maybe get_filepaths ?
def parse_pathnames(input_str: str) -> List:
    """This is a docstring.
    """
    
    try:  # check if input string is in list format
        pathnames = ast.literal_eval(input_str)
        if not isinstance(pathnames, list):
            raise ValueError
    except (SyntaxError, ValueError):  # else split the string manually
        pattern = r'(?<=\.(?:xml|tsv|txt))(?=\s|$)(?!\w)'
        pathnames = re.split(pattern, input_str) 
    # Strip extraneous characters that the user may have typed
    pathnames = [p.strip("', []") for p in pathnames if p.strip()]

    tsv_data, txt_data, xml_data = [], [], []
    for p in pathnames:
        ext = p[-3:].lower()  # last 3 characters = (file extension)
        if ext == "tsv": tsv_data.extend(parse_tsv(filepath=p))
        elif ext == "txt": txt_data.extend(parse_txt(filepath=p))
        elif ext == "xml": xml_data.extend(parse_xml(filepath=p))
    # TODO combine/sort the data
    return pathnames

if __name__ == "__main__":
    input_str = input("Please enter a list of pathnames: ")
    pathnames = parse_pathnames(input_str)
    print(f'pathnames: {pathnames}')