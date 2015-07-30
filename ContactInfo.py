##########################################################
# A simple ContactInfo class that complies with the
# IContactInfo interface from the specs.
# It holds the a Contact's info: name, phone & email.
##########################################################
class ContactInfo:
    def __init__(self, name=None, phone=None, email=None):
        self.name = name
        self.phone = phone
        self.email = email

    def getName(self):
        return self.name

    def getPhoneNumber(self):
        return self.phone

    def getEmailAddress(self):
        return self.email

    # The default way an instance of this class is printed
    def __str__(self):
        return "Name: {}\nPhone: {}\nEmail: {}".format(
            self.name, self.phone, self.email)
