#!/usr/bin/env python3
import sys
import os

if __name__=='__main__':

    file_name = ""
    if len(sys.argv) < 2:
        print("usage: filter_pi_estimates.py <file_name>")
    else:
        file_name = sys.argv[1]

    if os.path.exists(file_name):

        current_file = open(file_name)
        current_file_content = current_file.read().split("\n")

        for line in current_file_content:
            if line.startswith("3.1"):
                print(line)

        sys.exit(0)
    else:
        print("%s was not found" % file_name)
        sys.exit(1)
