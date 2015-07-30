#!/usr/bin/python

import unittest, BusinessCardParser
from BusinessCardParser import BusinessCardParser

class BusinessCardParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = BusinessCardParser()

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

    def testExtractNameInferredLastname(self):
        self.assertEqual(self.parser.extractName('Joe noname'),
            'Joe Noname')

    def testExtractNameFoundPairsHavePriority(self):
        self.assertEqual(self.parser.extractName('Joe noname Doe Joe'),
            'Joe Doe')




    def testExtractNameNoName(self):
        self.assertIsNone(self.parser.extractName('Title Software Engineer'))
        self.assertIsNone(self.parser.extractName('Assymetrik Company'))
        self.assertIsNone(self.parser.extractName('123-456-7890'))
        self.assertIsNone(self.parser.extractName('joe.doe@email'))



if __name__ == '__main__':
    unittest.main()