
import Borland
import EmbarcaderoClang
import VisualStudio
import Gcc
import Cpplint
from pathlib import Path
import util 
import fnmatch
from chardet.universaldetector import UniversalDetector

#Used for parsing an entire file.  The file parser just loads the correct type of line parser,
#and uses it to iterate over an entire file.
class FileParser(object):
    supportedflavors = ["gcc", "borland", "visualstudio","cpplint","embarcaderoclang"]
    parsers = [Gcc.GccLineParser, Borland.BorlandLineParser, VisualStudio.VisualStudioLineParser, 
               Cpplint.CpplintLineParser, EmbarcaderoClang.EmbarcaderoClangLineParser]
    all_warnings = [Gcc.all_warnings, Borland.all_warnings, VisualStudio.all_warnings, 
               Cpplint.all_warnings, EmbarcaderoClang.all_warnings]

    totalwarninglines = 0
    discoveredwarnings = None
    warninghashes = None
    flavor = None

    #create the File parser, given the 'flavor' of warnings expected
    #this is basically a line parser factory pattern.
    def __init__(self, flavor):
        if flavor in self.supportedflavors:
            self.flavor = flavor
            self.discoveredwarnings = set()
            self.warninghashes = list()
        else:
            raise ValueError

    #read a logfile given by filename
    #make discovered paths relative to the folder given by the 'relativeto' argument
    def readFile(self, filename, relativeto = None):
        if (self.flavor) == None:
            raise ValueError

        lineparser = dict(zip(self.supportedflavors, self.parsers))

        #determine file encoding
        detector = UniversalDetector()
        with open(filename, 'rb') as f:
            for line in f:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
        
        #open logfile and start looking for warnings 
        with open(filename, 'r', encoding=detector.result['encoding']) as f:
            for line in f:
                parser = lineparser[self.flavor]()    #here is where the line parser is called based on flavor
                parser.setLine(line)
                parser.parseLine()
                w = parser.getWarningObject()
                if w != None:
                    if relativeto != None:
                        w.fullpath = util.getpathfrom(w.fullpath, relativeto)
                    self.totalwarninglines += 1
                    self.discoveredwarnings.add(w)
        
        # Open each file once for all the warnings that come from the file.
        for file in self.getUniqueFiles():
            self.getWarningLines(file)

    #update all warnings from one particular file in case of error
    def updateWarningsInFile(self, filename:Path, message):
        warnings_in_this_file = self.getWarningsByFullpath(filename)
        for warn in warnings_in_this_file:
            warn.warningline = message
            warn.fileopened = False        

    #get lines of code from the files that had warnings
    def getWarningLines(self, filename):
        warn = None
        f = None
        try:
            f = open(Path(filename),'r', encoding='utf-8', errors='ignore')
        except FileNotFoundError:
            self.updateWarningsInFile(Path(filename), "warning_scraper error: could not open file")
            return

        #read file, should not be decoding errors since we are ignoring them in the open() call
        lines = f.readlines()
        f.close()

        #get lines of code from file
        warnings_in_this_file = self.getWarningsByFullpath(filename)
        for warn in warnings_in_this_file:
            try:
                warn.warningline = lines[warn.linenumber - 1].strip()  #the line of code, with leading and trailing whitespace stripped
                warn.fileopened = True
            #this means we could not get the line number we wanted
            except IndexError:
                if warn != None:
                    warn.warningline = "warning_scraper error: line not found in file"
                    warn.fileopened = False

    #get a list of unique warning IDs.  With this list plus getWarningsByWarningId() you can get a list of warnings by ID
    def getUniqueWarningIds(self):
        warningids = set()
        for warning in self.discoveredwarnings:
            warningids.add(warning.warningid)
        result = list(warningids)
        result.sort()
        return result

    #given all files that were found, show only unique files.  With this list plus getWarningsByFullpath() you can get a list of warnings by file
    def getUniqueFiles(self):
        files = set()
        for warning in self.discoveredwarnings:
            files.add(warning.fullpath)
        result = list(files)
        result.sort()
        return result

    #given the filename only, find all warnings for that file
    def getWarningsByFilename(self, filename:Path):
        results = list()
        for warning in self.discoveredwarnings:
            if warning.fullpath.name.lower() == filename.name.lower():
                results.append(warning)
        results.sort()
        return results

    #given the full path to a file, find all warnings for that file
    def getWarningsByFullpath(self, filename:Path):
        results = list()
        for warning in self.discoveredwarnings:
            try:
                if warning.fullpath == filename:
                    results.append(warning)
            except AttributeError:
                print("AttributeError --> debugme")
        results.sort()
        return results

    #given a warning ID, get all warnings with that ID
    def getWarningsByWarningId(self, warningid):
        results = list()
        for warning in self.discoveredwarnings:
            if warning.warningid == warningid:
                results.append(warning)
        results.sort()
        return results

    #given a warning ID, get the official warning description
    def getWarningDescriptionFromId(self, warningid):
        result = "(no warning description available)"
        flavor_to_warningdict = dict(zip(self.supportedflavors, self.all_warnings))
        warningdict = flavor_to_warningdict[self.flavor]

        if warningid in warningdict.keys():
            result = warningdict[warningid].description
        
        return result

    def getWarningSeverityFromId(self, warningid):
        result = "(no warning description available)"
        flavor_to_warningdict = dict(zip(self.supportedflavors, self.all_warnings))
        warningdict = flavor_to_warningdict[self.flavor]

        if warningid in warningdict.keys():
            result = warningdict[warningid].severity.name
        
        return result

    def removeExcludedWarnings(self, excludedFile = None):
        if excludedFile == None:
            return
        else:
            with open(Path(excludedFile), 'r') as f:
                warningstoremove = set()
                lines = f.read().splitlines()
                for warning in self.discoveredwarnings:
                    for line in lines:
                        if fnmatch.fnmatch(warning.fullpath, line):
                            warningstoremove.add(warning)
                for warning in warningstoremove:
                    self.discoveredwarnings.remove(warning)
            return