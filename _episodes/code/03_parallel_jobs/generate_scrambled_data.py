#!/usr/bin/env python3
import sys
import numpy as np

np.random.seed(2017)

def inside_circle(total_count):

    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    count = len(radii[np.where(radii<=1.0)])

    return count, x, y

if __name__=='__main__':

    n_samples = 4*1024*1024

    file_name = "pi_estimate.log"

    if "help" in " ".join(sys.argv):
        print("usage: generate_scrambled_data.py <optional:file_name>")
        print("""\n       script generates file <file_name> of 0.5 GB
       that contains blocks of random bytes followed
       by a newline and an estimate of pi""")
        sys.exit(0)

    if len(sys.argv) > 1:
        file_name = sys.argv[1]

    sizeof = np.dtype(np.float32).itemsize
    targetsize_byte = .5*1024*1024*1024
    string_to_write = ""
    loop_count = 0

    while len(string_to_write) < targetsize_byte :
        count, data, more  = inside_circle(n_samples)
        string_to_write += str(data.tostring())
        string_to_write += str(more.tostring())
        pi_estimate = (4.0 * count / n_samples)
        string_to_write += ("\n%f\n" % pi_estimate)
        if loop_count % 10 == 0:
            print(">> %f GB generated" % (len(string_to_write)/(1024*1024*1024.)))
        loop_count += 1

    print(">> storing %f GB to %s" % (len(string_to_write)/(1024*1024*1024.),file_name))
    fh = open(file_name,"w")
    fh.writelines(string_to_write)
    fh.close()
    sys.exit(0)
