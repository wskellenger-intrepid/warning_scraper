### 20-Feb-2021
Implementation following the specification located [here](https://docs.gitlab.com/ee/user/project/merge_requests/code_quality.html#implementing-a-custom-tool)

At the time of this writing, only the following properties are supported, the rest are ignored by gitlab.

* description
  * A description of the code quality violation.
* fingerprint
  * A unique fingerprint to identify the code quality violation. For example, an MD5 hash.
* severity
  * A severity string (can be info, minor, major, critical, or blocker).
* location.path
  * The relative path to the file containing the code quality violation.
* location.lines.begin
  * The line on which the code quality violation occurred.

