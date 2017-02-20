---
title: "Computing the answer to life, the universe and everything"
teaching: 30
exercises: 10
questions:
- "How do I exploit parallelism using MPI?"
objectives:
- - "Perform a calculation of pi on multiple nodes with 8 CPUs in total."
- "Perform a serial analysis on a lot of large files to extract a given text token."
- "Map the serial execution of independent analysis steps onto a cluster of compute nodes that are connected by a parallel file system."
key points:
- "The estimation of pi with the monte carlo method is a compute bound problem as the generation of pseudo random numbers consumes the most time, thus the generation of random numbers needs to be parallelized."
- "Scanning a file for text tokens is bound by the speed at which a file can be read."
- "Scanning a number of files for the same text token is a i/o bound problem. To speed it up, the input of files needs to be parallelized, i.e. the result for each file is independent of each other and thus it can be performed in parallel (this is the map step of map-reduce)."
- "After all files have been scanned, the results need to be collected (this is the reduce step of map-reduce)."
---
