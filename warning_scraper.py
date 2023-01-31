import argparse
import sys
import os
from FileParser import FileParser
from Warning import Warning
from pathlib import Path
import util
import jinja2
import html

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--logfile", help="logfile to read as input", type=Path)
    parser.add_argument("--flavor", help="the logfile flavor: (borland, cppcheck, gcc)")
    parser.add_argument("--gitsha", help="git sha of the parent repo for the source code")
    parser.add_argument("--outputfile", help="the output filename", type=Path)
    parser.add_argument("--format", help="format for output report (html, gitlab_json)", default="html")
    parser.add_argument("--urlrelativeto", help="file URLs will be relative to this folder")
    # the urlbase argument is something like:
    # http://your.gitlab.server.corp/root/projectname/-/blob
    parser.add_argument(
        "--urlbase", help="the base URL path to locate the report artifact on your Gitlab server")
    parser.add_argument("--excludelist", help="path to the textfile containing files or directories to be included in wildcard format")
    args = parser.parse_args()

    if len(sys.argv) == 1:
       parser.print_help()
       sys.exit()

    return args

def get_script_path():
    """
    Get the path of this script, which is where templates are
    """
    if (__name__ == "__main__"):
        return os.path.dirname(os.path.realpath(sys.argv[0]))
    else:
        return "."

def writeReport(args, fp):
    # get template environment ready
    md5_written = set()  #used inside the json template to track which warnings were written

    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        get_script_path() + '/template/'), trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)
    
    if (args.format == "html"):
        template = jinja_env.get_template('html/top_html.jinja')
    elif (args.format == "gitlab_json"):
        template = jinja_env.get_template('json/gitlab_code_quality.jinja')
    else:
        print("Error -- unknown format specified: {0}".format(args.format))
        template = None
        sys.exit(1)

    with open(args.outputfile, 'wb') as outfile:
        output_templ = template.render(fp=fp, md5_written=md5_written, len=len, args=args, getpathfrom=util.getpathfrom, hex=hex, cleanforjson=util.cleanforjson, htmlescape=html.escape)
        print("Writing: {0}".format(outfile.name))
        output_encoded = bytes(output_templ, 'utf-8')
        outfile.write(output_encoded)

def checkReport(args, fp):
    if (args.format == "gitlab_json"):
        print("Validating json: {0}".format(args.outputfile))
        valid = util.validate_json(args.outputfile)
        if (valid == False):
            print("Generated json is invalid, please examine the json file with a json lint tool to debug.")
            sys.exit(1)

def main():
    args = getargs()
    fp = FileParser(args.flavor)
    fp.readFile(args.logfile, args.urlrelativeto)
    fp.removeExcludedWarnings(args.excludelist)
    writeReport(args, fp)
    checkReport(args, fp)


if __name__ == "__main__":
    main()
