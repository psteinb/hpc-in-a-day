---
title: "Parallel Estimation of Pi for Pedestrians"
teaching: 45
exercises: 10
questions:
- "How do I use multiple cores on a computer to solve a problem?"
objectives:
- "Perform a calculation of pi using only one CPU core."
- "Perform a calculation of pi using multiple CPU cores on one machine."
- "Measure the run time of both the serial and parallel version of the implementation and compare them."
keypoints:
- "The estimation of pi with the Monte Carlo method is a compute bound problem."
- "The generation of pseudo random numbers consumes the most time."
- "The generation of random numbers can be parallelized."
- "Time consumption of a single application can be measured using the `time` utility."
- "The ratio of the run time of a parallel program divided by the time of the equivalent serial implementation, is called speed-up."
---

Lola is told that her predecessors all worked on the same project. A high performance calculation that is able to produce a high precision estimate of Pi. Even though calculating Pi can be considered a solved problem, this piece of code is used at the institute to benchmark new hardware. So far, the institute has only acquired larger single machines for each lab to act as work horse per group. But currently, need for distributed computations has arisen and hence a distributed code is needed, that yields both simplicity, efficiency and scalability. 

The algorithm to implement is very simple. It was pioneered by _Georges-Louis Leclerc de Buffon_ in _1733_. 

![Estimating Pi with Buffon's needle](../tikz/estimate_pi.svg)

Overlay a unit square over a quadrant of a circle. Throw `m` random number pairs and count how many of the pairs lie inside the circle (the number pairs inside the circle is denoted by `n`). `Pi` is then approximated by: 

~~~
     4*m
Pi = ---
      n
~~~

The implementation of this algorithm using `total_count` random number pairs in a nutshell is given in the below program:

~~~
import numpy

np.random.seed(2017)

def inside_circle(total_count):
    
    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    count = len(radii[np.where(radii<=1.0)])
    
    return count 
    
def estimate_pi(total_count):

    return (4.0 * inside_circle(total_count) / total_count) 
    
~~~
{: .python}

This code is already written in a way to allow later reuse in parallel applications. So don't mind the two-fold indirection where `estimate_pi` calls `inside_circle`. For generating pseudo-random numbers, we sample the uniform probability distribution in the default floating point interval from `0` to `1`. The `sqrt` step is not required directly, but Lola includes it here for clarity. `numpy.where` is used obtain the list of indices that correspond to radii which are equal or smaller than `1.0`. At last, this list of indices is used to filter-out the numbers in the `radii` array and obtain its length, which is the number Lola are after.

Lola finishes writing the pi estimation and comes up with a [small python script](code/03_parallel_jobs/serial_numpi.py), that she can launch from the command line:

~~~
$ python3 ./serial_numpi.py 1000000000
~~~
{: .bash}

~~~
[serial version] required memory 11444.092 MB
[serial version] pi is 3.141557 from 1000000000 samples
~~~
{: .output}

She must admit that the application takes quite long to finish. Yet another reason to use a cluster or any other remote resource for these kind of applications that take quite a long time. But not everyone has a cluster at his or her disposal. So she decides to parallelize this algorithm first so that it can exploit the number cores that each machine on the cluster or even her laptop has to offer.

> ## Premature Optimisation is the root of all evil!
>
> Before venturing out and trying to accelerate a program, it is utterly important to find the hot spots of it by means of measurements. For the sake of this tutorial, we use the [line_profiler](https://github.com/rkern/line_profiler) of python. Your language of choice most likely has similar utilities.
> 
> In order to install the profiler, please call:
> ~~~
> $ pip3 install line_profiler
> ~~~
> {: .bash }
> 
> When this is done, you have to annotate your code in order to indicate to the profiler what you want to profile. For this, we change the `inside_circle` function definition:
> 
> ~~~
> ...
> @profile
> def inside_circle(total_count):
>   ...
> ~~~
> 
> Let's save this to `serial_numpi_annotated.py`. After this is done, the profiler is run with a reduced input parameter that does take only about 2-3 seconds:
> 
> ~~~
> $ kernprof-3.5 -l ./serial_numpi_annotated.py 50000000
> [serial version] required memory 572.205 MB
> [serial version] pi is 3.141728 from 50000000 samples
> Wrote profile results to serial_numpi_annotated.py.lprof
> ~~~
> {: .bash }
> 
> You can see that the profiler just adds one line to the output, i.e. the last line. In order to view, the output we can use the line_profile module in python:
> 
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
$ time python3 ./serial_numpi.py 1000000000
~~~
{: .bash}

~~~
[serial version] required memory 11444.092 MB
[serial version] pi is 3.141557 from 1000000000 samples

real    0m52.305s
user    0m40.444s
sys     0m11.655s
~~~
{: .output}

~~~
$ time python3 ./parallel_numpi.py 1000000000
~~~
{: .bash}
~~~
[parallel version] required memory 11444.092 MB
[using  12 cores ] pi is 3.141631 from 1000000000 samples

real    0m12.113s
user    2m10.676s
sys     0m34.477s
~~~
{: .output}

If the snipped from above is compared to the snippets earlier, you can see that `time` has been put before any other command executed at the prompt and 3 lines have been added to the output of our program. `time` reports 3 times and they are all different:

  - `real` that denotes the time that has passed during our program as if you would have used a stop watch
  - `user` this is accumulated amount of CPU seconds (so seconds that the CPU was active) spent in code by the user (you)
  - `sys`  this is accumulated amount of CPU seconds that the CPU spent while executing system code that was necessary to run your program (memory management, display drivers if needed, interactions with the disk, etc.)
    
So from the above, Lola wants to compare the `real` time spent by her serial implementation (`0m52.305s`) and compare it to the `real` time spent by her parallel implementation (`0m12.113s`). Apparently, her parallel program was _4.3_ times faster than the serial implementation. The latter number is called the speed-up of the parallelization. Very good for a first attempt. 

> ## Adding up times
> The output of the `time` command is very much bound to how a operating system works. In an ideal world, `user` and `sys` of serial programs should add up to `real`. Typically they never do. The reason is, that the operating systems used in HPC and on laptops or workstations are set up in a way, that the operating system decides which process receives time on the CPU (aka to perform computations) when. Once a process runs, it may however happen, that the system decides to intervene and have some other binary have a tiny slice of a CPU second while your application is executed. This is where the mismatch for `user+sys` and `real` comes from.
> Note also how the `user` time of the parallel program is a lot larger than the time that was actually consumed. This is because, time reports accumulated timings i.e. it adds up CPU seconds that were consumed in parallel.
{: .callout}

> ## Something is missing
> A speed-up of _8.6x_ for a parallel python program is not bad. The luxury of python programming makes us pay the price of performance. In a perfect world, data parallel algorithms using one machine only are expected to scale perfectly, i.e. using 20 cores should give a speed-up of _20x_. Due to a myriad of reasons from the software or from the hardware side, this perfect scaling often remains a hard-to-achieve goal which projects attain only after months if not years of development.
{: .callout}
