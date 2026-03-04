# warning_scraper
A python script to scrape compiler warnings and generate summary reports.
* William Skellenger (wskellenger@intrepidcs.com)
* February 2021
* Matthew Loehr (mloehr@intrepidcs.com)
* May 2021
* Paul Abbott [@phatpaul](https://github.com/phatpaul)
* Jan 2026

## Motivation

* The borland compiler is still somewhat widely used by legacy projects.  However, warning scraping support for this compiler is neglected even
by large plugins like [warnings-ng](https://plugins.jenkins.io/warnings-ng/) for Jenkins.
* The Gitlab development environment has support for 'code quality', but it requires a proprietary json format as input.
* The Gitlab development enviornment, at this point in time, [has no support](https://gitlab.com/gitlab-org/gitlab/-/issues/293954) for scraping compiler warnings.

Given the above, we needed a way to scrape warnings from the neglected Borland compiler, and output them into the proprietary json format 
required by Gitlab's code quality feature.

The tool was designed to be flexible enough to support warnings from other compilers/tools as well.  Support for Borland, Visual Studio, and gcc warning "flavors" is provided.

## Prerequisites

* Python 3.8+ 

Additional Python modules required:

* jinja2 -- template engine
* pyparsing -- powerful parsing framework
* chardet -- encoding detector

### (Optional) Install 
Install the tool and its dependencies with **pipx**:

```sh
cd warning_scraper/
pipx install .
```

Or install with **uv**:

```sh
cd warning_scraper/
uv tool install .
```

Now you can just run it on the command line. I.e.:

`warning_scraper --help`


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
--exit-nonzero-on-warnings: exit with non-zero code if warnings are detected (useful for CI/CD)
--print-warnings: print warnings to console output
```

Example invocation:
```sh
warning_scraper.py --logfile whatever.txt --flavor borland --gitsha abcd12342 --format html --outputfile out.html
```

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

### exit-nonzero-on-warnings (added January 2025)

When the `--exit-nonzero-on-warnings` flag is specified, the tool will exit with a non-zero return code (1) if any warnings are detected, and exit with code 0 (success) only when no warnings are found.

This is particularly useful in CI/CD environments where you want the build pipeline to indicate failure when warnings are present.

### print-warnings (added March 2026)

When the `--print-warnings` flag is specified, all scraped warnings will be printed to the console in a human-readable format, organized by file and line number.

This is useful if you want to view warnings directly in the log output without downloading report artifacts. You can use this flag:
- **Alone**: To only print warnings to console (omit `--outputfile`)
- **With `--outputfile`**: To both print warnings and generate a report file

Example for console-only output:
```sh
warning_scraper --logfile build.log --flavor gcc --print-warnings
```

Example for both console and report:
```sh
warning_scraper --logfile build.log --flavor gcc --print-warnings --outputfile report.json --format gitlab_json
```

## Example Gitlab CI

 For example, in GitLab CI you can use:

```yaml
build-job:
  stage: build
  script:
    # create build dir for tee output
    - mkdir -p build
    # split the build output to a log file for later code quality analysis
    - idf.py build | tee build/build_log.txt
  artifacts:
    paths:
      - build/
    expire_in: 1 day

code-quality-job:
  image: python:3.12
  stage: code_quality
  needs:
    - job: build-job
      artifacts: true
  script:
    # In this example, the warning_scraper tool is available in the project repository. Install it from here.
    - cd ${CI_PROJECT_DIR}/tools/warning_scraper
    - pip install .
    # Run python script to parse the build log and generate code quality report
    # The --print-warnings flag will display warnings in the job log for easy viewing
    - warning_scraper --logfile ${FW_DIR}/build/build_log.txt --flavor gcc --format gitlab_json --output ${FW_DIR}/build/code_quality_report.json --print-warnings --exit-nonzero-on-warnings
  artifacts:
    paths:
      - ${FW_DIR}/build/code_quality_report.json
    reports:
      codequality: ${FW_DIR}/build/code_quality_report.json
    expire_in: 1 day
  # allow to fail so that code quality issues do not block the pipeline, but are still reported
  allow_failure: true
```

The `allow_failure: true` setting ensures that:
- The pipeline continues even when warnings are found
- The job is marked as failed/warning state when warnings exist  
- Artifacts are still uploaded when the job fails
- The overall pipeline status reflects the warning condition
