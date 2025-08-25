# Identify filenames with characters outside the Basic Multilingual Plane.
# Tested on a Windows 2008 host using python 3.4. until 3.8.1, Python 2.7 does not work.

import os
import os.path
import sys

# Change following line to update the version for testing and validating
if sys.version_info[0] != 3 or sys.version_info[1] != 8:
    sys.stderr.write("!!! Python 3.8 required !!!")
    exit(1)

# In a rough test, consider anything larger than MAX_UTF8 as non-BMP.
MAX_UTF8 = 0xffff

if len(sys.argv) < 2:
    sys.stderr.write("Please specify one or more paths to traverse.\n")
    exit(1)

def print_if_non_bmp(path, entry, isdir=False):
    for c in entry:
        if ord(c) > MAX_UTF8:
            fullpath = os.path.join(path, entry)
            if isdir:
                fullpath = os.path.join(fullpath, "")
            try:
                print(fullpath)
            except UnicodeEncodeError:
                print(str(fullpath.encode("utf-8")) + " (UTF-8 ENCODED)")
            return 1
    return 0

if len(sys.argv) < 2:
    sys.stderr.write("Please specify a path to traverse.\n")
    exit(1)

non_bm_files = 0
for top in sys.argv[1:]:
    sys.stderr.write("--> Traversing %s\n" % repr(top))
    for path, dirs, files in os.walk(top):
        for d in dirs:
            non_bm_files += print_if_non_bmp(path, d, isdir=True)
        for f in files:
            non_bm_files += print_if_non_bmp(path, f)

if non_bm_files > 0:
    errmsg = (80 * "=") + "\n"
    errmsg += "Found %u filenames outside BMP\n" % non_bm_files
    sys.stderr.write(errmsg)

