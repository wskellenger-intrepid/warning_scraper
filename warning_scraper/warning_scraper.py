import argparse
import sys
import os
from .FileParser import FileParser
from .Warning import Warning
from pathlib import Path
from . import util
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
    parser.add_argument("--exit-nonzero-on-warnings", action="store_true",
                        help="exit with non-zero code if warnings are detected (useful for CI/CD)")
    parser.add_argument("--print-warnings", action="store_true",
                        help="print warnings to console output")
    args = parser.parse_args()

    if len(sys.argv) == 1:
       parser.print_help()
       sys.exit()

    return args

def get_script_path():
    """
    Get the path of this script, which is where templates are
    """
    return os.path.dirname(os.path.realpath(__file__))

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

def printWarnings(fp):
    """Print warnings to console in a readable format"""
    if len(fp.discoveredwarnings) == 0:
        print("\nNo warnings found.")
        return

    print(f"\n{'='*80}")
    print(f"Found {len(fp.discoveredwarnings)} warning(s):")
    print(f"{'='*80}")

    # Sort warnings by file path, then line number
    sorted_warnings = sorted(fp.discoveredwarnings,
                            key=lambda w: (str(w.fullpath), w.linenumber))

    current_file = None
    for idx, w in enumerate(sorted_warnings, 1):
        # Print file header when it changes
        if current_file != w.fullpath:
            current_file = w.fullpath
            print(f"\n{w.fullpath}")

        # Print warning details
        print(f"  Line {w.linenumber}:{w.colnumber if w.colnumber != -1 else '?'} [{w.severity.name.upper()}] {w.warningid}")
        print(f"    {w.warningmessage}")
        if w.warningline and w.fileopened:
            print(f"    Code: {w.warningline}")
        print()

    print(f"{'='*80}")

def main():
    args = getargs()
    fp = FileParser(args.flavor)
    fp.readFile(args.logfile, args.urlrelativeto)
    fp.removeExcludedWarnings(args.excludelist)

    # Print warnings to console if requested
    if args.print_warnings:
        printWarnings(fp)

    # Generate report file if output file is specified
    if args.outputfile:
        writeReport(args, fp)
        checkReport(args, fp)
    elif not args.print_warnings:
        print("Warning: No output file specified and --print-warnings not enabled. No output generated.")

    # Exit with non-zero code if warnings are found and the flag is set
    if args.exit_nonzero_on_warnings and len(fp.discoveredwarnings) > 0:
        print(f"Found {len(fp.discoveredwarnings)} warning(s), exiting with non-zero code")
        sys.exit(1)


if __name__ == "__main__":
    main()
