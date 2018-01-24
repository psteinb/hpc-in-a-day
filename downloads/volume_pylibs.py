from __future__ import print_function

import os
import sys
import glob
import re

def pylibs_files():
    """ searchs for the path seen by python (aka sys.path) which contains os.py and return all paths to .py therein as a list"""

    path_of_ospy = ""
    text = []

    for d in sys.path:
        if os.path.isdir(d) and os.path.exists(d+"/os.py"):
            path_of_ospy = d
            break

    if not path_of_ospy or not os.path.exists(path_of_ospy):
        print("no modules found in "+sys.path)
        return text

    std_files = glob.glob(path_of_ospy+"/*.py")

    return std_files

def bytes_on_disk(fname):
    """ return the number of bytes this file requires on disk  """

    if os.path.exists(fname):
        return os.stat(fname).st_size
    else:
        return 0

def main():

    libs = pylibs_files()
    nbytes = 0

    for path in libs:
        nbytes += bytes_on_disk(path)

    print("%i B of standard python libraries found" % (nbytes))

    if nbytes:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
