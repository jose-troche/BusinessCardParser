#!/usr/bin/python

import re, string
from ContactInfo import ContactInfo

##########################################################
# BusinessCardParser: It has the logic to parse a
# documnet and extract name, phone and email from it
# The main class of the solution. 
##########################################################
class BusinessCardParser:

    ##########################################################################
    # Constructor: Initializes sets and regular expressions used by the parser
    ##########################################################################
    def __init__(self):
        # The first and last names are loaded into sets for super fast lookup O(1)
        # (Files adapted from:
        # https://www.sajari.com/public-data?amp;q.sl=1&q.id=d48du3lo8bldmqod&q.sl=1)
        self.firstNames = self._loadFileIntoSet('firstNames.txt')
        self.lastNames = self._loadFileIntoSet('lastNames.txt')
        
        # Fax reg ex is used to discard fax numbers
        self.faxRegEx = re.compile(r'fax')

        # Because of output format, numbers are assumed to be in groups of 3, 3 & 4
        self.phoneRegEx = re.compile(
            r'\(?([0-9]{3})\)?[-. ]?\(?([0-9]{3})\)?[-. ]?\(?([0-9]{4})\)?')
        
        # Email regular expression from:
        #   http://www.w3.org/TR/html5/forms.html#valid-e-mail-address
        self.emailRegEx = re.compile(
            r'[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*')

    #########################################################################
    # This is the main entry point an conforms to the
    # interface IBusinessCardParser from the spec
    # It traverses the document looking for the name, phone and email
    #########################################################################
    def getContactInfo(self, document):
        for line in document:
            # We assume name, phone, and/or email may be on the same line
            name = extractName(line)
            phone = extractPhone(line)
            email = extractEmail(line)

            # No need to look further if we have them all
            if name and phone and email:
                break
            
        return ContactInfo(name, phone, email)

    ########################################################
    # Searches and extracts a valid phone from a string line
    ########################################################
    def extractPhone(self, line):
        # Ignore lines that include Fax
        if self.faxRegEx.search(line, re.IGNORECASE):
            return None
        found = self.phoneRegEx.search(line)
        return '{0}-{1}-{2}'.format(found.group(1), found.group(2), found.group(3)) if found else None

    ########################################################
    # Searches and extracts a valid email from a string line
    ########################################################
    def extractEmail(self, line):
        found = self.emailRegEx.search(line)
        return found.group(0) if found else None

    #####################################################
    # Searches and extracts a name from a string line
    # Assumption: a name is firstname+lastname or
    # lastname+firstname (no middle name nor initial)
    #####################################################
    def extractName(self, line):
        # Get a list of lowercased words without punctuation
        words = [word.strip(string.punctuation).lower() for word in line.split()]
        lenWords = len(words)

        # Need at least two words (one firstname, one lastname)
        if lenWords < 2: 
            return None

        name = None

        ### Scan for names ###
        # General idea: There is a dictionary of common first and last names.
        # Search for a first name (present in the firstNames dictionary/set) 
        # immediately followed by a last name (present in the lastNames 
        # dictionary/set) or a last name immediately followed by a first name.
        # If only one is found, assume the next/previous word is the other one
        # and cache the result. If a combination is found later, that one has
        # priority, otherwise return the cached name. at the end.
        for i in xrange(lenWords):
            if words[i] in self.firstNames: # Current word is a firstname
                if i < lenWords-1:
                    # Next word is possibly a lastname
                    name = self._formatName(words[i], words[i+1])
                    if words[i+1] in self.lastNames: # If found as lastname, return
                        return name
                else: # At last word, then the previous word should be a lastname
                    return self._formatName(words[i], words[i-1])
            elif words[i] in self.lastNames: # Current word is a lastname
                if i < lenWords-1:
                    if words[i+1] in self.firstNames: # If next word is firstname, return
                        return self._formatName(words[i+1], words[i])
                    else: 
                        if i > 0: # We assume that previous word was an non-recognized firstname
                            name = self._formatName(words[i-1], words[i])
                        else: # First word, then assume next is an non-recognized firstname
                            name = self._formatName(words[i+1], words[i])
                else: # At last word, then the previous word should be a firstname
                    return self._formatName(words[i-1], words[i])

        return name

    # Private method to format the name according to specs
    def _formatName(self, firstName, lastName):
        return (firstName + ' ' + lastName).title()

    # Private method to load words of a file into a set for fast O(1) look ups
    def _loadFileIntoSet(self, filename):
        itemSet = set()
        with open(filename, 'r') as f:
            for item in f: # read one line at a time
                if item:
                    itemSet.add(item.strip()) # Add into set stripping LF/CR
        return itemSet

if __name__ == '__main__':
    cardParser = BusinessCardParser()
    print cardParser.extractPhone('Phone: (410)555-1234')
    print cardParser.extractEmail('Phone: (410)555-1234')
    print cardParser.extractName('This is lisa haug the Software dev')
    print cardParser.extractEmail('Email: lisa.haung@foobartech.subdomain.io')
    print ContactInfo('Jose', '123-456-7890', 'j@email.com')