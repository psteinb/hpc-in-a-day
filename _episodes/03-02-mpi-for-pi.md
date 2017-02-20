---
title: "Computing the answer to life, the universe and everything"
teaching: 30
exercises: 10
questions:
- "How do I exploit parallelism using MPI?"
objectives:
- "Perform a calculation of pi using one node, but all cores of it."
- "Perform a calculation of pi on multiple nodes with 8 CPUs in total."
- "Perform a serial analysis on a lot of large files to extract a given text token."
- "Map the serial execution of independent analysis steps onto a cluster of compute nodes that are connected by a parallel file system."
key points:
- "The estimation of pi with the monte carlo method is a compute bound problem as the generation of pseudo random numbers consumes the most time, thus the generation of random numbers needs to be parallelized."
- "Scanning a file for text tokens is bound by the speed at which a file can be read."
- "Scanning a number of files for the same text token is a i/o bound problem. To speed it up, the input of files needs to be parallelized, i.e. the result for each file is independent of each other and thus it can be performed in parallel (this is the map step of map-reduce)."
- "After all files have been scanned, the results need to be collected (this is the reduce step of map-reduce)."
---


Lola is told that her predecessors all worked on the same project. A high performant calculation that is able to produce a high precision estimate of Pi. Even though calculating Pi can be considered a solved problem, this piece of code is used at the institute to benchmark new hardware. So far, the institute has only aquired larger single machines for each lab to act as work horse per group. But currently, need for distributed computations has arisen and hence a distributed code is needed, that yields both simplicity, efficiency and scalability. 

The algorithm to implement is very simple. It was pioneered by Georges-Louis Leclerc de Buffon in 1733. 

![Estimating Pi with Buffon's needle](../tiks/estimate_pi.svg)

Overlay a unit square over a quadrant of a circle. Throw `m` random number pairs and count how many of the pairs lie inside the circle (the number pairs inside the cirlce is denoted by `n`). `Pi` is then approximated by: 

```{bash}
     4*m
Pi = ---
      n
```

The implementation of this algorithm using 10000 random number pairs in a nutshell is given in the below program:

```{python}
#!/usr/bin/env python3

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
    
```

One of the simplest approaches of making a program faster, is trying to compute as many parts as possible in parallel. In this case here, we can make the observation that each iteration of the for loop is independent of each other. This renders itself as prime candidate for parallelisation. Lola starts by converting the program into an application that can exploit all available cores as it is sometimes easier to experiment on your laptop first and then deploying a larger application onto a cluster.


