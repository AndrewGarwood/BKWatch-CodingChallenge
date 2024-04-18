import json
import re
from typing import List



filepath = 'input3-sample.txt'

def parse_txt(filepath: str) -> List:
    txt_data = []
    with open(filepath, 'r') as file:
        file_data = file.read()
        file_data.strip()
        # regular expressions for extracting different parts of the address
        address_pattern = r'(?P<name>.+)\n(?P<street>.+)\n(?:\n?(?P<county>[A-Z\s]+) COUNTY\n)?(?P<city>[^\d\n]+),\s*(?P<state>[A-Za-z]+),?\s*(?P<zip>\d{5}(?:-\d{4})?)'
        
        match_list = list(re.finditer(address_pattern, file_data))
        for match in match_list:
            address_dict = match.groupdict()
            txt_data.append(address_dict)
        for key in address_dict.keys():
            address_dict[key] = address_dict[key].strip()
        return txt_data
    

result = parse_txt('input3-sample.txt')
print(f'result:\n{json.dumps(result, sort_keys=False, indent=2)}')
