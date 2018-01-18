---
title: "Parallel Estimation of Pi for Pedestrians"
teaching: 45
exercises: 10
questions:
- "How do I use multiple cores on a computer to solve a problem?"
objectives:
- "Perform a calculation of pi using multiple CPU cores on one machine."
- "Measure the run time of both the parallel version of the implementation and compare it to the serial one."
keypoints:
- "The estimation of pi with the Monte Carlo method is a compute bound problem."
- "The generation of pseudo random numbers consumes the most time."
- "The generation of random numbers can be parallelized."
- "Time consumption of a single application can be measured using the `time` utility."
- "The ratio of the run time of a parallel program divided by the time of the equivalent serial implementation, is called speed-up."
---

> ~~~
> $ python3 -m line_profiler serial_numpi_profiled.py.lprof
> Timer unit: 1e-06 s
> 
> Total time: 2.40138 s
> File: ./serial_numpi_profiled.py
> Function: inside_circle at line 7
> 
> Line #      Hits         Time  Per Hit   % Time  Line Contents
> ==============================================================
>      7                                           @profile
>      8                                           def inside_circle(total_count):
>      9                                           
>     10         1       827103 827103.0     34.4      x = np.float32(np.random.uniform(size=total_count))
>     11         1       891397 891397.0     37.1      y = np.float32(np.random.uniform(size=total_count))
>     12                                           
>     13         1       322505 322505.0     13.4      radii = np.sqrt(x*x + y*y)
>     14                                           
>     15         1       360375 360375.0     15.0      count = len(radii[np.where(radii<=1.0)])
>     16                                           
>     17         1            4      4.0      0.0      return count
> ~~~
> {: .output }
>
> So generating the random numbers appears to be the bottleneck as it accounts for 70% of the time. So this is a prime candidate for acceleration.
>
{: .callout}


One of the many ways of making a program faster, is trying to compute as many independent parts as possible in parallel. In this case here, we can make the observation that each pair of numbers in `x` and `y` is independent of each other. 

![Illustration of drawing random number pairs `x` and `y` and their dependency](../tikz/data_parallel_estimate_pi.svg)

Keeping this in mind, splitting up the work for multiple cores requires Lola to split up the number of total samples by the number of cores available and calling `count_inside` on each of these partitions.

![Partitioning `x` and `y`](../tikz/partition_data_parallel_estimate_pi.svg)

The number of partitions has to be limited by the number of CPU cores available. With this in mind, the `estimate_pi` method can be converted to run in parallel:

~~~
from multiprocessing import Pool

def estimate_pi(n_samples,n_cores):

    partitions = [ ]
    for i in range(n_cores):
        partitions.append(int(n_samples/n_cores))

    pool = Pool(processes=n_cores)
    counts=pool.map(inside_circle, partitions)

    total_count = sum(partitions)
    return (4.0 * sum(counts) / total_count)

~~~
{: .python}

We are using the `multiprocessing` module that comes with the python standard library. The first step is to create a list of numbers that contain the partitions. For this, `n_samples` is divided by the number of cores available on the machine, where this code is executed. The ratio has to be converted to an integer to ensure, that each partition is compatible to a length of an array. The construct used next is a process `Pool`. Due to technical details on how the python interpreter is built, we do not use a Pool of threads here. In other languages than python, `threads` are the more common idiom to represent independent strings of execution that share the same memory than the process they are created in. The process `Pool` creates `n_cores` processes and keeps them active as long as the `Pool` is active. Then `pool.map` will call `inside_circle` using an item of `partitions` as the argument. In other words, for each item in `partitions`, the `inside_circle` function is called once using the respective item as input argument. The result of these invocations of `inside_circle` are stored within the `counts` variable (which will have the same length as `partitions` eventually).

![Partitioning `x` and `y` and results of reach partition](../tikz/partition_data_parallel_estimate_pi_with_results.svg)

The last step required before calculating pi is to collect the individual results from the `partitions` and _reduce_ it to one `total_count` of those random number pairs that were inside of the circle. Here the `sum` function loops over `partitions` and does exactly that. So let's run our [parallel implementation](code/03_parallel_jobs/parallel_numpi.py) and see what it gives:

~~~
$ python3 ./parallel_numpi.py 1000000000
~~~
{: .bash}

~~~
[parallel version] required memory 11444.092 MB
[using  20 cores ] pi is 3.141631 from 1000000000 samples
~~~
{: .output}

The good news is, the parallel implementation is correct. It estimates Pi to equally bad precision than our serial implementation. The question remains, did we gain anything? For this, Lola tries to the `time` system utility that can be found on all *nix installations and most certainly on compute clusters.

~~~
$ time python3 ./serial_numpi.py 200000000
~~~
{: .bash}

~~~
[serial version] required memory 2288.818 MB
[serial version] pi is 3.141604 from 200000000 samples

real	0m12.766s
user	0m10.543s
sys		0m2.101s
~~~
{: .output}

~~~
$ time python3 ./parallel_numpi.py 2000000000
~~~
{: .bash}

~~~
[parallel version] required memory 2288.818 MB
[using  12 cores ] pi is 3.141642 from 200000000 samples

real	0m1.942s
user	0m12.097s
sys		0m2.813s
~~~
{: .output}

If the snipped from above is compared to the snippets earlier, you can see that `time` has been put before any other command executed at the prompt and 3 lines have been added to the output of our program. `time` reports 3 times and they are all different:

  - `real` that denotes the time that has passed during our program as if you would have used a stop watch
  - `user` this is accumulated amount of CPU seconds (so seconds that the CPU was active) spent in code by the user (you)
  - `sys`  this is accumulated amount of CPU seconds that the CPU spent while executing system code that was necessary to run your program (memory management, display drivers if needed, interactions with the disk, etc.)
    
So from the above, Lola wants to compare the `real` time spent by her serial implementation (`0m52.305s`) and compare it to the `real` time spent by her parallel implementation (`0m12.113s`). Apparently, her parallel program was _4.3_ times faster than the serial implementation. The latter number is called the speed-up of the parallelization. Very good for a first attempt. 


> ## Adding up times
> The output of the `time` command is very much bound to how a operating system works. In an ideal world, `user` and `sys` of serial programs should add up to `real`. Typically they never do. The reason is, that the operating systems used in HPC and on laptops or workstations are set up in a way, that the operating system decides which process receives time on the CPU (aka to perform computations). Once a process runs, it may however happen, that the system decides to intervene and have some other binary have a tiny slice of a CPU second while your application is executed. This is where the mismatch for `user+sys` and `real` comes from.
> Note also how the `user` time of the parallel program is a lot larger than the time that was actually consumed. This is because, `time` reports accumulated timings i.e. it adds up CPU seconds that were consumed in parallel.

