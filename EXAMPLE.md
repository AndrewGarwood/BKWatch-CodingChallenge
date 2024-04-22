# Example Usage (of current progress; there is still work to do)

## This file contains an example of running challenge.py from the command line

### The Process

#### Open the terminal, run program

`python C:\path\to\challenge.py`

#### program prompts the user for input

I accounted for various types of input one might type in:
The user may type the list of paths in different ways. (i.e. different separators, whitespace, with/without braces) (example separators: ' ', '', ',',  ', ', . . etc.)
Example 1:: `path1\file1.xml path2\file2.tsv path3\file3.txt`
Example 2: `[path1\file1.xml, path2\file2.tsv, path3\file3.txt]`
Example 3: `path1\file1.xmlpath2\file2.tsvpath3\file3.txt`

Note:
an objective of mine is to implement main() with ArgumentProcessor so that one
can instead type:
`python C:\path\to\challenge.py path1 path2. . . pathN`

#### program outputs formatted data

### Example of running program from command line

[user] `python C:\path\to\challenge.py`
[console] `"Please enter a list of path(s): "`
[user] `input1-sample.xml, input2-sample.tsv, input3-sample.txt`
[console]
[
  {
    "organization": "OneSource Service, Inc.",
    "street": "135 West 20th Street Suite 201",
    "city": "New York",
    "state": "NY",
    "zip": "10011-3648"
  },
  {
    "name": "James Joseph Moley,Jr.",
    "street": "136 Third Street",
    "city": "Saint James",
    "state": "NY",
    "zip": "11780"
  },
  {
    "organization": "Rincon Jimenez Enterprises LLC",
    "street": "6191 W Atlantic Blvd # 1",
    "city": "Margate",
    "state": "Florida",
    "zip": "33063"
  },
  {
    "organization": "Hillsboro Petroleum West, Inc.",
    "street": "19323 Skyridge Cir.",
    "city": "Boca Raton",
    "state": "FL",
    "zip": "33498"
  },
  {
    "name": "Sonji S Dixon-McCoy",
    "street": "1222 East 146th Street",
    "city": "Dolton",
    "state": "Illinois",
    "zip": "60419"
  },
  {
    "name": "Daniel Kaleta",
    "street": "7236 W 62nd St",
    "city": "Summit Argo",
    "state": "Illinois",
    "zip": "60501"
  },
  {
    "organization": "Artisan Builders, LLC",
    "street": "14362 N. Frank Lloyd Wright Blvd., #1000",
    "city": "Scottsdale",
    "state": "AZ",
    "zip": "85260-8847"
  },
  {
    "name": "Maria De Los Angeles Najera",
    "street": "10340 Canoga Ave, Apt 220",
    "city": "Chatsworth",
    "state": "California",
    "county": "Los Angeles",
    "zip": "91311-2281"
  },
  {
    "name": "David Scherrep",
    "street": "12014 Cobblewood Lane North",
    "county": "DUVAL",
    "city": "Jacksonville",
    "state": "Florida",
    "zip": "99999-9999"
  }
]

--------
Still work to do, but this is something
