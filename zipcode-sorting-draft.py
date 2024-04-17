import json
from typing import List

# basic case: input is list of JSON objects in format:
# goal: sort objects by zip code in ascending order. return sorted list
# get zip1=object1['zip']. zip2=object2['zip'] delete any hyphens in zips
# if comparing zip1 & zip2

object_list = [
  {
    "name": "Hilda Flores",
    "street": "1509 Alberbrook Pl",
    "city": "Garland",
    "county": "DALLAS",
    "state": "TX",
    "zip": "75040"
  },
  {
    "organization": "Central Trading Company Ltd.",
    "street": "1501 North Division Street",
    "city": "Plainfield",
    "state": "Illinois",
    "zip": "60544-3890"
  }
]

# Step 1: Extract Zip Codes and Remove Hyphens
def extract_zip(obj):
  zip_code = obj.get('zip', '')  # Get the zip code from the object
  return zip_code.replace('-', '')  # Remove hyphens if present

# Step 2: Custom Sorting Key Function
def sorting_key(obj):
  return extract_zip(obj)

# Step 3: Sorting
sorted_list = sorted(object_list, key=sorting_key)

# Step 4: Result
print(json.dumps(sorted_list, indent=2))

'''
sorted(iterable, key=None, reverse=False)
- iterable: The iterable (e.g., list, tuple, string) to be sorted.
- key (optional): A function that specifies the sorting criteria. It
  takes an element from the iterable as input and returns a value based
  on which the sorting is done. If not provided, elements are sorted
  based on their natural order.
- reverse (optional): A boolean value indicating whether to sort in
  reverse order (descending) or not. Default is False (ascending order).
'''