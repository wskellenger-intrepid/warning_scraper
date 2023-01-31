
from pathlib import Path
import json

def stripleadingrelativefrom(inputf:Path):
    result = Path("")
    founddotdot = 0
    if ("..") in inputf.parts[0]:
        #get rid of leading ../../.. if relative path
        for index, part in enumerate(inputf.parts):
            #this will only work if they are contiguous .. found at the start
            if (founddotdot == index) and (part == ".."):
                founddotdot += 1
            else:
                result = result.joinpath(part)
    else:
        result = inputf
    return result

#given c:/whatever/this/thing/is/not/foo.py
#and provided "thing" in argument frompos
#return "/is/not/foo.py" if include = False
#return "thing/is/not/foo.py" if include = True
def getpathfrom(inputf:Path, frompos:str, include=False)->Path:
    result = Path("")
    if (frompos != None):
        try:
            idx = inputf.parts.index(frompos)
            if include == False:
                idx += 1
            for part in inputf.parts[idx:]:
                result = result.joinpath(part)
        except ValueError:
            result = stripleadingrelativefrom(inputf)

    return result

#taken from
#https://stackoverflow.com/questions/54491156/validate-json-data-using-python
def validate_json(filename):
    with open(filename) as file:
        try:
            json.load(file) # put JSON-data to a variable
        except json.decoder.JSONDecodeError:
            return False
        else:
            return True


#cleanups for json
def cleanforjson(text:str):
    #get rid of stray backslash
    if "\\" in text:
        text = text.replace("\\", "\\\\")

    if r'"' in text:
        text = text.replace(r'"', r"'")

    
    return text
