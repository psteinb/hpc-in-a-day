#!/usr/bin/env python3
import sys
import os

if __name__=='__main__':

    file_name = ""
    if len(sys.argv) < 2:
        print("usage: count_pi_estimates.py <file_name>")
    else:
        file_name = sys.argv[1]

    if os.path.exists(file_name):
        print("opening", file_name)

        current_file = open(file_name)
        current_file_content = current_file.read().split("\n")
        count = 0
        for line in current_file_content:
            if line.startswith("3.1"):
                count += 1

        print(count)
        sys.exit(0)
    else:
        print("%s was not found" % file_name)
        sys.exit(1)
