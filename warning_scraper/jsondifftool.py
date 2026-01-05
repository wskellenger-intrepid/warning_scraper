import json
import sys
from pathlib import Path
import operator

def getwarningwithfprint(warnings, fprint):
    output = None
    for w in warnings:
        if w["fingerprint"] == fprint:
            output = w
            break
    return output

def getwarningsbyfile(warnings):
    warnings_by_file = dict()
    for w in warnings:
        path = w["location"]["path"]
        if path in warnings_by_file.keys():
            warnings_by_file[path].append(w)
        else:
            warnings_by_file[path] = list()
            warnings_by_file[path].append(w)
    return warnings_by_file


def main():
    fixedwarning = list()
    newwarning = list()

    file1 = Path(sys.argv[1])
    file2 = Path(sys.argv[2])

    with open(file1) as f1:
        j1 = json.load(f1)
    with open(file2) as f2:
        j2 = json.load(f2)

    j1fingerprints = [x["fingerprint"] for x in j1]
    j2fingerprints = [x["fingerprint"] for x in j2]
    j1fingerprints.sort()
    j2fingerprints.sort()

    for fprint in j1fingerprints:
        if fprint not in j2fingerprints:
            fixedwarning.append(getwarningwithfprint(j1, fprint))

    for fprint in j2fingerprints:
        if fprint not in j1fingerprints:
            newwarning.append(getwarningwithfprint(j2, fprint))

    print ("{0} warnings fixed, {1} new warnings".format(len(fixedwarning), len(newwarning)))

    fixedwarning_sorted = sorted(fixedwarning, key=lambda x: (x["location"]["path"], x["location"]["lines"]["begin"]))
    newwarning_sorted = sorted(newwarning, key=lambda x: (x["location"]["path"], x["location"]["lines"]["begin"]))

    fixedwarning_by_file = getwarningsbyfile(fixedwarning_sorted)
    newwarning_by_file = getwarningsbyfile(newwarning_sorted)

    allfiles = list()
    allfiles.extend(list(fixedwarning_by_file.keys()))
    allfiles.extend(list(newwarning_by_file.keys()))

    for key in allfiles:
        print("--- File: {0}".format(key))

        try:
            fixed = len(fixedwarning_by_file[key])
            print("Fixed: ({0})".format(fixed))
        except KeyError:
            fixed = 0
            print("Fixed: (0)")

        try:
            for w in fixedwarning_by_file[key]:
                print("{0}, {1}:{2}".format(w["description"], w["location"]["path"], w["location"]["lines"]["begin"]))
        except KeyError:
            print("")

        print("")

        try:
            new = len(newwarning_by_file[key])
            print("New: ({0})".format(new))
        except KeyError:
            new = 0
            print("New: (0)")

        try:
            for w in newwarning_by_file[key]:
                print("{0}, {1}:{2}".format(w["description"], w["location"]["path"], w["location"]["lines"]["begin"]))
        except KeyError:
            print("")

        if (new > fixed):
            print("+++ increased warnings")
        if (new < fixed):
            print("--- decreased warnings")

        print("")
    

if __name__ == "__main__":
    main()