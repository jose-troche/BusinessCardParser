# Business Card Parser

## Prerequisites
* Python 2.7 (This will not work on Python 3). Tested on Windows and Mac. Will probably work with no problems in Linux.

## Files Description

* BusinessCardParser.py: The main class. It has the logic to parse a document and extract its information (name, phone & email). It reads from standard input and outputs the extracted information. To execute: 
```
python BusinessCardParser.py < Card.txt

Name: Arthur Wilson
Phone: 703-555-1259
Email: awilson@abctech.com
```

* BusinessCardParserTests.py: Unit and integration tests. To execute:
```
python BusinessCardParserTests.py
```

* Card.txt: A Sample input file

* ContactInfo.py: A class that holds the information of a Contact (name, phone & email). This class complies with the IContactInfo interface from the specs. 

* firstNames.txt: A list of common First Names

* lastNames.txt: A list of common Last Names

Note: The first and last names were obtained from https://www.sajari.com/public-data?amp;q.sl=1&q.id=d48du3lo8bldmqod&q.sl=1 and then adapted.