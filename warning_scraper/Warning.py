import hashlib
from enum import Enum

#severity definitions
class Severity(Enum):
    info = 1
    minor = 2
    major = 3
    critical = 4
    blocker = 5

#this is more like a struct
#description: this is the "OFFICIAL" description from the compiler vendor
#severity: severity of warning (this is somewhat subjective, can be altered for your own needs)
#warningid: identifier of warning from compiler vendor
class OfficialWarningDesc(object):
    description = None
    severity = None
    warningid = None

    def __init__(self, warningid, description, severity):
        self.warningid = warningid
        self.description = description
        self.severity = severity

#this is a simple class that holds information about a warning.
#it has an equality operator as well as a hash operator.
#The hash operator is used (for example) when trying to put many warnings objects into a set()
#this class represents everything that was scraped while parsing the warning output
class Warning(object):
    colnumber = -1
    linenumber = -1
    warningid = ""
    warningmessage = ""
    fullpath = ""
    warningline = ""
    fileopened = False
    severity = None

    #equality operator
    def __eq__(self, other):
        equal = False
        if (other != None):
            if (self.colnumber == other.colnumber) and (self.linenumber == other.linenumber) and (self.warningid == other.warningid) and (self.fullpath == other.fullpath):
                equal = True
        return equal

    #hash this value, is used by Python for efficient equality determination
    def __hash__(self):
        #we will only use the filename here (and not full path), because on the CI runner the path will differ from build to build
        return hash((self.colnumber, self.linenumber, self.warningid, self.fullpath.name))

    #lessthan operator, used when sorting
    def __lt__(self, other):
        lt = False
        if (other != None):
            if (self.warningid <= other.warningid) and (self.fullpath <= other.fullpath) and (self.linenumber <= other.linenumber):
                lt = True
        return lt

    #md5 hash of specific contents in the warning object.  This is used when generating a 'fingerprint' for Gitlab json
    def md5(self, uselinenumber=False, usecolnumber=False):
        linecolnumber = ''
        #concatenate line number/col number if desired by caller
        if (uselinenumber==True):
            linecolnumber += str(self.linenumber)
        if (usecolnumber==True):
            linecolnumber += str(self.colnumber)

        if (uselinenumber == True) or (usecolnumber == True) or (self.fileopened == False):
                #we use the line number in the md5 hash if we don't have the line of code
                hashstr = self.warningmessage + self.warningid + self.warningline + self.fullpath.name + linecolnumber
        else:
            #we use the actual line of code in the hash if we have it
            hashstr = self.warningmessage + self.warningid + self.warningline + self.fullpath.name

        md5 = hashlib.md5(bytes(hashstr, "utf8"))
        return md5.hexdigest()
