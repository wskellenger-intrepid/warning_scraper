# warning_scraper
A python script to scrape compiler warnings and generate summary reports.
* William Skellenger (wskellenger@intrepidcs.com)
* February 2021
* Matthew Loehr (mloehr@intrepidcs.com)
* May 2021

## Motivation

* The borland compiler is still somewhat widely used by legacy projects.  However, warning scraping support for this compiler is neglected even
by large plugins like [warnings-ng](https://plugins.jenkins.io/warnings-ng/) for Jenkins.
* The Gitlab development environment has support for 'code quality', but it requires a proprietary json format as input.
* The Gitlab development enviornment, at this point in time, [has no support](https://gitlab.com/gitlab-org/gitlab/-/issues/293954) for scraping compiler warnings.

Given the above, we needed a way to scrape warnings from the neglected Borland compiler, and output them into the proprietary json format 
required by Gitlab's code quality feature.

The tool was designed to be flexible enough to support warnings from other compilers/tools as well.  Support for Borland, Visual Studio, and gcc warning "flavors" is provided.

## Prerequisites

* Python 3.6+ 

Additional Python modules required:

* jinja2 -- template engine
* pyparsing -- powerful parsing framework
* chardet -- encoding detector

## Running the tool

warning_scraper.py: the main program

command-line options:
```
--help: help for options
--logfile: the log file to scrape
--flavor: the type of warnings to expect (borland, visualstudio, gcc)
--gitsha: the git sha of the build where the reports came from, will be used to generate links to the repository
--format: the type of output (html, gitlab_json) to produce
--outputfile: the name of the output file
--urlbase: the base URL where the report artifact will be found (something like http://server.company.corp/root/project/-/blob)
--urlrelativeto: will truncate the discovered file paths such that they are relative to this directory, more info below
--excludelist: a text file containing a list of files that should be exlcluded from warnings.  The list can contain wildcards.
```

Example invocation:
warning_scraper.py --logfile whatever.txt --flavor borland --gitsha abcd12342 --format html --outputfile out.html

## Explanation of arguments

### urlrelativeto

If a warning was discovered in `C:\cirunner\12345\path\to\project\src\module\module.cpp`, you could 
specify `--urlrelativeto project` at the commandline to store the path as relative to 'project', so you'd get
`src\module\module.cpp` instead.

### excludelist (added August 2021)

Provide the path to a text file that contains a list of exclusions.  An example text file might look like this:

```
*/ExternalLibraries/*
*/rad studio/*
```

It should also accept entries like:

```
*/Windows*.cpp
*/Windows*.h
```
