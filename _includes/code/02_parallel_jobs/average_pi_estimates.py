#!/usr/bin/env python3
import sys
import os

if __name__=='__main__':

    files = []
    if len(sys.argv) < 2:
        print("usage: average_pi_estimates.py <file_name>")
        sys.exit(1)
    else:
        files = sys.argv[1:]

    pi_estimates_as_strings = []
    for f in files:
        if os.path.exists(f):

            current_file = open(f)
            current_file_content = current_file.read().split("\n")

            for line in current_file_content:
                if line.startswith("3.1"):
                    pi_estimates_as_strings.append(line)

    pi_estimates = []
    for s in pi_estimates_as_strings:
        pi_estimates.append(float(s))

    print("averaged value of pi from %i estimates : %f" % (len(pi_estimates),sum(pi_estimates)/len(pi_estimates)))
    sys.exit(0)
