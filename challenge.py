import re
import ast
import json
from typing import List

# PEP **8** Style Guide Notes: (will delete this later)
# Limit all lines to a maximum of 79 characters.
# For(docstrings or comments), limit to 72 characters.
# Inline comments should be separated by at least two spaces from the
# statement. They should start with a # and a single space.

def parse_tsv(filepath: str) -> List:
  return # list of JSON objects

def parse_txt(filepath: str) -> List:
  return # list of JSON objects

def parse_xml(filepath: str) -> List:
  return # list of JSON objects

# could rename this to process_input or something more descriptive
def parse_pathnames(input_str: str) -> List:
  """This is a docstring.
  """
  

  # check if input string is in list format
  try:
    pathnames = ast.literal_eval(input_str)
    if not isinstance(pathnames, list):
      raise ValueError
  except (SyntaxError, ValueError):
    # If parsing fails, split the string manually
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
  print(pathnames)