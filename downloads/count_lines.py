from __future__ import print_function

import os
import sys


def lines_count(afilename):
    """ counts the number of words in the string given by <text> """

    if not os.path.exists(afilename):
        return 0

    return len(open(afilename).readlines())

def main():

    if len(sys.argv)<2:
        print("usage: python count_lines.py <file(s)>)")
        sys.exit(1)

    total = 0
    for infile in sys.argv[1:]:
        len_ = lines_count(infile)
        print(len_,infile)
        total += len_

    print(total,"total")
    sys.exit(0)

if __name__ == '__main__':
    main()
