import re

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
    def __init__(self):
        # First and last names from:
        # https://www.sajari.com/public-data?amp;q.sl=1&q.id=d48du3lo8bldmqod&q.sl=1
        self.firstNames = self.loadFileIntoSet('firstNames.txt')
        self.lastNames = self.loadFileIntoSet('lastNames.txt')
        self.phoneRegEx = re.compile(
            r'\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})')
        # Email regular expression from:
        #   http://www.w3.org/TR/html5/forms.html#valid-e-mail-address
        self.emailRegEx = re.compile(
            r'[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*')

    # document is a list of strings
    def getContactInfo(self, document):
        return parse(document)

    def parse(document):
        for line in document:
            # We assume name, phone, and/or email may be on the same line
            name = extractName(line)
            phone = extractPhone(line)
            email = extractEmail(line)

            # No need to look further if we have them all
            if name and phone and email:
                break
            
        return ContactInfo(name, phone, email)

    def extractName(self, line):
        words = line.split()
        for i in xrange(len(words)-1):
            word = words[i].lower()
            nextWord = words[i+1].lower()
            if word in self.firstNames and nextWord in self.lastNames:
                return self.getCapitalizedName(word, nextWord)

            if word in self.lastNames and nextWord in self.firstNames:
                return self.getCapitalizedName(nextWord, word)

        return None

    def getCapitalizedName(self, firstName, lastName):
        return firstName.capitalize() + ' ' + lastName.capitalize()

    def extractPhone(self, line):
        found = self.phoneRegEx.search(line)
        return '{0}-{1}-{2}'.format(found.group(1), found.group(2), found.group(3)) if found else None

    def extractEmail(self, line):
        found = self.emailRegEx.search(line)
        return found.group(0) if found else None

    # Load words of a file into a set
    def loadFileIntoSet(self, filename):
        itemSet = set()
        with open(filename, 'r') as f:
            for item in f: # read one line at a time
                if item:
                    itemSet.add(item.strip()) # Strip new lines
        return itemSet

cardParser = BusinessCardParser()
print cardParser.extractPhone('Phone: (410)555-1234')
print cardParser.extractEmail('Phone: (410)555-1234')
print cardParser.extractName('This is haung lisa the Software dev')
print cardParser.extractEmail('Email: lisa.haung@foobartech.subdomain.io')