import re
from typing import List

def parse_pathnames(input_str: str) -> List:
  files = []
  pattern = r' ,|\s|(?=[\[\]])|(?<=[\[\]])' # [1]


  return files

if __name__ == "main":
  input_str = input("Please enter a list of pathnames: ")
  pathnames = parse_pathnames(input_str)