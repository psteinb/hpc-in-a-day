#!/usr/bin/env python3
import sys
import random
import math

def estimate_pi(total_count):

    count_inside = 0
    for count in range(0, total_count):
        x = random.random()
        y = random.random()
        d = math.sqrt(x*x + y*y)
        if d < 1: count_inside += 1

    estimate = 4.0 * count_inside / total_count
    return estimate

if __name__=='__main__':

    n_iterations = 10000
    if len(sys.argv) > 1:
        n_iterations = int(sys.argv[1])

    my_pi = estimate_pi(n_iterations)

    print("[serial version] pi is %f from %i samples" % (my_pi,n_iterations))
