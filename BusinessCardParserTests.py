#!/usr/bin/python

import unittest, BusinessCardParser
from BusinessCardParser import BusinessCardParser

class BusinessCardParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = BusinessCardParser()

    ########################
    # Unit Tests
    ########################

    ## Email
    def testExtractEmailSorroundedByText(self):
        self.assertEqual(
            self.parser.extractEmail('This email joe.doe@nomail.io is Joe\'s'),
            'joe.doe@nomail.io')

    def testExtractEmailTwoEmails(self):
        # Expect just first one
        self.assertEqual(
            self.parser.extractEmail('joe.doe@nomail.io and john@test.com'),
            'joe.doe@nomail.io')

    def testExtractEmailWithSubdomain(self):
        self.assertEqual(
            self.parser.extractEmail('joe.doe@nomail.subdomain.io'),
            'joe.doe@nomail.subdomain.io')

    def testExtractEmailWithSingleDomain(self):
        self.assertEqual(
            self.parser.extractEmail('joe.doe@io'),
            'joe.doe@io')

    def testExtractEmailInvalidEmail(self):
        self.assertIsNone(self.parser.extractEmail('joe.doe@@nomail'))
        self.assertIsNone(self.parser.extractEmail('joe.doenomail'))
        self.assertIsNone(self.parser.extractEmail('joe@.nomail'))
        self.assertIsNone(self.parser.extractEmail('joe @nomail'))

    ## Phones
    # Because of output format numbers are assumed to be in groups of 3, 3 & 4
    def testExtractPhonePlain(self):
        self.assertEqual(
            self.parser.extractPhone('1234567890'), '123-456-7890')

    def testExtractPhoneWithDots(self):
        self.assertEqual(
            self.parser.extractPhone('123.456.7890'), '123-456-7890')

    def testExtractPhoneWithDashes(self):
        self.assertEqual(
            self.parser.extractPhone('123-456-7890'), '123-456-7890')

    def testExtractPhoneWithMixedSeparators(self):
        self.assertEqual(
            self.parser.extractPhone('(123).456-7890'), '123-456-7890')

    def testExtractPhoneWithSomeParenthesis(self):
        self.assertEqual(
            self.parser.extractPhone('(123)4567890'), '123-456-7890')

    def testExtractPhoneWithAllParenthesis(self):
        self.assertEqual(
            self.parser.extractPhone('(123)(456)(7890)'), '123-456-7890')

    def testExtractPhoneIgnoreFaxNumbers(self):
        self.assertIsNone(self.parser.extractEmail('Fax: 123-456-7890'))
        self.assertIsNone(self.parser.extractEmail('123-456-7890 (Fax)'))

    ## Names
    def testExtractNameFirstNameFirst(self):
        self.assertEqual(self.parser.extractName('Here\'s a name: Joe Doe'),
            'Joe Doe')

    def testExtractNameLastNameFirst(self):
        self.assertEqual(self.parser.extractName('Name: Doe, Joe (lastname, firstname)'),
            'Joe Doe')

    def testExtractNameInferredLastName(self):
        self.assertEqual(self.parser.extractName('Joe noname'),
            'Joe Noname')

    def testExtractNameCombinationHasPriority(self):
        self.assertEqual(self.parser.extractName('Joe noname Doe Joe'),
            'Joe Doe')
        self.assertEqual(self.parser.extractName('Joe noname Joe Doe'),
            'Joe Doe')

    def testExtractNameFirstNameAsLastWord(self):
        self.assertEqual(self.parser.extractName('Name: noname Joe'),
            'Joe Noname')

    def testExtractNameLastNameAsLastWord(self):
        self.assertEqual(self.parser.extractName('Name: noname Doe'),
            'Noname Doe')

    def testExtractNameLastNameAsFirstWord(self):
        self.assertEqual(self.parser.extractName('Doe noname is here'),
            'Noname Doe')

    def testExtractNameInferredFirstName(self):
        self.assertEqual(self.parser.extractName('Name: noname Doe'),
            'Noname Doe')

    def testExtractNameSingleWord(self):
        self.assertIsNone(self.parser.extractName('Joe'))
        self.assertIsNone(self.parser.extractName('Doe'))

    def testExtractNameNoName(self):
        self.assertIsNone(self.parser.extractName('Title Software Engineer'))
        self.assertIsNone(self.parser.extractName('ACME Company'))
        self.assertIsNone(self.parser.extractName('123-456-7890'))
        self.assertIsNone(self.parser.extractName('joe.doe@email'))


    ########################
    # Integration Tests
    ########################
    def testCard1(self):
        card = """
            ASYMMETRIK LTD
            Mike Smith
            Senior Software Engineer
            (410)555-1234
            msmith@asymmetrik.com
        """
        self._checkResults(card, 'Mike Smith', '410-555-1234', 'msmith@asymmetrik.com')

    def testCard2(self):
        card = """
            Foobar Technologies
            Analytic Developer
            Lisa Haung
            1234 Sentry Road
            Columbia, MD 12345
            Phone: 410-555-1234
            Fax: 410-555-4321
            lisa.haung@foobartech.com
        """
        self._checkResults(card, 'Lisa Haung', '410-555-1234', 'lisa.haung@foobartech.com')

    def testCard3(self):
        card = """
            Arthur Wilson
            Software Engineer
            Decision & Security Technologies
            ABC Technologies
            123 North 11th Street
            Suite 229
            Arlington, VA 22209
            Tel: 703-555-1259
            Fax: 703-555-1200
            awilson@abctech.com
        """
        self._checkResults(card, 'Arthur Wilson', '703-555-1259', 'awilson@abctech.com')

    def _checkResults(self, card, expectedName, expectedPhone, expectedEmail):
        contact = self.parser.getContactInfo(card.split('\n'))
        self.assertEqual(contact.getName(), expectedName)
        self.assertEqual(contact.getPhoneNumber(), expectedPhone)
        self.assertEqual(contact.getEmailAddress(), expectedEmail)


if __name__ == '__main__':
    unittest.main()