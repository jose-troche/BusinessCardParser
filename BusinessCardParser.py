#!/usr/bin/python

import re, string

class ContactInfo:
    def __init__(self, name=None, phone=None, email=None):
        self.name = name
        self.phone = phone
        self.email = email

    def getName(self):
        return self.name

    def getgetPhoneNumber(self):
        return self.phone

    def getEmailAddress(self):
        return self.email

class BusinessCardParser:

    ##########################################################################
    # Constructor: Initializes sets and regular expressions used by the parser
    ##########################################################################
    def __init__(self):
        # The first and last names are loaded into sets for super fast lookup O(1)
        # (Files adapted from:
        # https://www.sajari.com/public-data?amp;q.sl=1&q.id=d48du3lo8bldmqod&q.sl=1)
        self.firstNames = self.loadFileIntoSet('firstNames.txt')
        self.lastNames = self.loadFileIntoSet('lastNames.txt')
        
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
    # interface IBusinessCardParser spec
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

    #################################################
    # Searches and extracts a name from a string line
    #################################################
    def extractName(self, line):
        # Get lowercase words without punctuation
        words = [word.strip(string.punctuation).lower() for word in line.split()]
        lenWords = len(words)

        # Need at least two words (one firstname, one lastname)
        if lenWords < 2: 
            return None

        # Try finding firstname + lastname or lastname + firstname
        for i in xrange(lenWords-1):
            word = words[i]
            nextWord = words[i+1]
            if word in self.firstNames and nextWord in self.lastNames:
                return self.getCapitalizedName(word, nextWord)

            if word in self.lastNames and nextWord in self.firstNames:
                return self.getCapitalizedName(nextWord, word)

        # If first and last name are not found try finding just one
        for i in xrange(lenWords):
            if words[i] in self.firstNames: 
                if i < lenWords-1: # Assume next is Last Name
                    return self.getCapitalizedName(words[i], word[i+1])
                else:
                    return self.getCapitalizedName(words[i], words[i-1])

            if words[i] in self.lastNames: 
                if i > 0: # Assume prior is First Name
                    return self.getCapitalizedName(words[i-1], words[i])
                else:
                    return self.getCapitalizedName(words[i+1], words[i])

        return None

    # Format the name according to specs
    def getCapitalizedName(self, firstName, lastName):
        return (firstName + ' ' + lastName).title()

    # Load words of a file into a set
    def loadFileIntoSet(self, filename):
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