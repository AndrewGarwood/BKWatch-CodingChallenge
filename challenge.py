import re
import ast
import csv
import json
from typing import List

# TODO: 
#       Add error handling for invalid file formats
#       clean up comments and docstrings
#       clean up everything for PEP 8 b/c this sh unsightly

# PEP **8** Style Guide Notes: (will delete this later)
# Limit all lines to a maximum of 79 characters.
# For(docstrings or comments), limit to 72 characters.
output_header = ['name', 'organization', 'address', 'city', 'state', 'county',
                 'zip', 'zip4']
def parse_tsv(filepath: str) -> List:
  result = []
  with open(filepath, 'r') as file:
    tsv_reader = csv.reader(file, delimiter="\t")   
    next(tsv_reader)  # skip the header row
    for row in tsv_reader:  # type(row) == list
      assert(row != [] and row != None)
      print(f'row={row}')  # who doesn't love print statements?
      row_data = {}
      # handle case where 'organization' is in 'last' column and vice versa    
      # and join the first, middle, and last names
      # then join zip and zip4
      row_name, is_org = get_name(row)
      if is_org: row_data['organization'] = row_name
      else: row_data['name'] = row_name
      for key, value in zip(output_header[2:6], row[4:8]):  # this ain't clean
        #  if key == 'name' or key == 'organization': continue
        if value != '' and value != 'N/A':
          row_data[key] = value     
      
      row_data['zip'] = handle_zip(zip=row[8], zip4=row[9])
      result.append(row_data)
      print(f'row_data:\n{json.dumps(row_data, sort_keys=False, indent=2)}')  
    return result # list of JSON objects

def parse_txt(filepath: str) -> List:
  return # list of JSON objects

def parse_xml(filepath: str) -> List:
  return # list of JSON objects
def get_name(row: List) -> str:
  first, middle, last, org = row[0], row[1], row[2], row[3]
  name = ''
  is_org = False

  if first and last:
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
    if ext == "tsv": tsv_data.append(parse_tsv(filepath=p))
    elif ext == "txt": txt_data.append(parse_txt(filepath=p))
    elif ext == "xml": xml_data.append(parse_xml(filepath=p))
  # then combine/sort the data
  return pathnames

if __name__ == "__main__":
  input_str = input("Please enter a list of pathnames: ")
  pathnames = parse_pathnames(input_str)
  print(f'pathnames: {pathnames}')


# The file formats are not documented, but you can deduce the formats by examing
# their contents. The challenge is to write a python script `challenge.py`,
# designed to be run from the command line, that accepts a list of pathnames of
# files in any of the above formats, parses them, and writes a JSON-encoded list
# of the combined addresses to standard output, sorted by ZIP code in ascending order. You can assume
# that the the format of each file corresponds to its extension, as illustrated by
# the above examples. Your submission should consist of a single file, without any 
# supporting documents. The output should be a pretty-printed JSON array of JSON
# objects, each having 5 or 6 properties, serialized in the given order:
#
# * `name`: The person's full name, if present, consisting of a list of one or more given names followed by the family name
# * `organization`: The company or organization name, if present
# * `street`: The street address, often just a house number followed by a direction indicator and a street name
# * `city`: The city name
# * `county:` The county name, if present
# * `state`: The US state name or abbreviation
# * `zip`: The ZIP code or ZIP+4, in the format 00000 or 00000-0000

# A personal name or organization name will always be present, but not both.

# Here is a sample output:

# ```
# [
#   {
#     "name": "Hilda Flores",
#     "street": "1509 Alberbrook Pl",
#     "city": "Garland",
#     "county": "DALLAS",
#     "state": "TX",
#     "zip": "75040"
#   },
#   {
#     "organization": "Central Trading Company Ltd.",
#     "street": "1501 North Division Street",
#     "city": "Plainfield",
#     "state": "Illinois",
#     "zip": "60544-3890"
#   }
# ]
# ```

# The script should

# * Be well-organized and easy to understand
# * Use only standard Python libraries
# * Be compatible with Python 3.11
# * Conform to [PEP 8](https://peps.python.org/pep-0008/)
# * Provide a `--help` option
# * Check for errors in the argument list
# * Check the input files to make sure they conform to the formats expemplified by the sample files 
# * Output a list of addresses only if no errors were discovered in the above two steps
# * Write any error messages to stderr
# * Exit with status `0` or `1` to indicate success or failure

# > [!WARNING]
# > Study the data carefully: it's not as easy as it looks.