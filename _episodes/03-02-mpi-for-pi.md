---
title: "Computing the answer to life, the universe and everything"
teaching: 45
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

![Estimating Pi with Buffon's needle](../tikz/estimate_pi.svg)

Overlay a unit square over a quadrant of a circle. Throw `m` random number pairs and count how many of the pairs lie inside the circle (the number pairs inside the cirlce is denoted by `n`). `Pi` is then approximated by: 

~~~
     4*m
Pi = ---
      n
~~~

The implementation of this algorithm using `total_count` random number pairs in a nutshell is given in the below program:

~~~
#!/usr/bin/env python3

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

> ## Editing a file on a remote machine
> If you are following the materials closely, this is the time where you might want to edit a file on your cluster and paste the contents of the code snippet above into it. The question is, how to do that?
>
> You have several options: 
> 1. run a editor inside the `ssh` session that you opened to work on the cluster (mostly vi/vim, emacs, nano or pico are programs commonly installed on HPC machines)
> 2. connect to the cluster with `ssh` using the ssh `-X` switch, if done so, you can open editors like emacs, nedit, gedit, ... that are capable of spinning up a GUI (careful though, the GUI contents need to be transmitted through the network from the cluster to your workstation or laptop and vice verse, so in case you have a poor network connection, this approach can be visually painful)
> 3. use remote editing capabilities of your preferred editor or IDE (emacs and vim has a built-in packages for this, check your preferred IDE manual for details)
> 4. have a folder of your remote host mounted on your laptop (the details depend on the remote cluster and you should get in touch with the admin to find out what technologies are available), edit the files inside this folder (most of the time they are updated to the clsuter in real-time) and launch the applications from your `ssh` session

Lola finishes writing the pi estimation and comes up with a [small python script](../samples/03_parallel_jobs/serial_numpi.py), that she can launch from the command line:

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

![Partitioning `x` and `y` and results of reach partition](../tikz/partition_data_parallel_estimate_pi_wit_results.svg)

The last step required before calculating pi is to collect the individual results from the `partitions` and _reduce_ it to one `total_count` of those random number pairs that were inside of the circle. Here the `sum` function loops over `partitions` and does exactly that. So let's run our [parallel implementation](../samples/03_parallel_jobs/parallel_numpi.py) and see what it gives:

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
[using  20 cores ] pi is 3.141631 from 1000000000 samples

real    0m6.113s
user    1m5.676s
sys     0m17.477s
~~~
{: .output}

If the snipped from above is compared to the snippets earlier, you can see that `time` has been put before any other command executed at the prompt and 3 lines have been added to the output of our program. `time` reports 3 times and they are all different:

    - `real` that denotes the time that has passed during our program as if you would have used a stop watch
    - `user` this is accumulated amount of CPU seconds (so seconds that the CPU was active) spent in code by the user (you)
    - `sys`  this is accumulated amount of CPU seconds that the CPU spent while executing system code that was necessary to run your program (memory management, display drivers if needed, interactions with the disk, etc.)
    
So from the above, Lola wants to compare the `real` time spent by her serial implementation (`0m52.305s`) and compare it to the `real` time spent by her parallel implementation (`0m6.113s`). Apparently, her parallel program was _8.6_ times faster than the serial implementation. The latter number is called the speed-up of the parallelisation. Very good for a first attempt. 

> ## Adding up times
> The output of the `time` command is very much bound to how a operating system works. In an ideal world, `user` and `sys` of serial programs should add up to `real`. Typically they never do. The reason is, that the operating systems used in HPC and on laptops or workstations are set up in a way, that the operating system decices which process receives time on the CPU (aka to perform computations) when. Once a process runs, it may however happen, that the system decides to intervene and have some other binary have a tiny slice of a CPU second while your application is executed. This is where the mismatch for `user+sys` and `real` comes from.
> Note also how the `user` time of the parallel program is a lot larger than the time that was actually consumed. This is because, time reports accumulated timings i.e. it adds up CPU seconds that were consumed in parallel.
{: .callout}

> ## Something is missing
> A speed-up of _8.6x_ for a parallel python program is not bad. The luxury of python programming makes us pay the price of performance. In a perfect world, data parallel algorithms using one machine only are expected to scale perfectly, i.e. using 20 cores should give a speed-up of _20x_. Due to a myriad of reasons from the software or from the hardware side, this perfect scaling often remains a hard-to-achieve goal which projects attain only after months if not years of development.
{: .callout}

To finalize this day's work, Lola wants to tackle distributed memory parallelisation using the Message Passing Interface (MPI). For this, she uses the `mpi4py` library that is preinstalled on her cluster. She again starts from the [serial implementation](../samples/03_parallel_jobs/serial_numpi.py). At first, she expands the include statements a bit. 

~~~
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
~~~
{: .python }

These 4 lines will be very instrumental through out the entire MPI program. The entire MPI software stack builds upon the notion of a communicator. Here, we see the MPI.COMM_WORLD communicator by which all processes that are created talk to each other. We will use it as a hub to initiate communications among all participating processes. Subsequently, we ask `comm` how many participants are connected by calling `comm.Get_size()`. Then we'll ask the communicator, what rank the current process is `comm.Get_rank()`. And with this, Lola has entered the dungeon of MPI. 

> ## Every Line Is Running in Parallel!
> As discussed in the previous section, a call to `<your scheduler> mpirun <your program>` will do the following:
>     - `mpirun` will obtain a list of available nodes from the scheduler
>     - mpirun will then `ssh` onto these nodes for you and instantiate a local mpirun there
>     - this local mpirun will execute `<your program>` in parallel to all the others and call every line of it from top to bottom
>     - only if your program reaches a statement of the form `comm.do_something(...)`, your program will start communicating through the mpi library with the other mpi processes; this communication can entail point-to-point data transfers or collective data transfers (that's why it's called 'message passing' because MPI does nothing else than provide mechanism to send messages around the cluster), depending on the type of communication, the MPI library might make your program wait until the all message passing has been completed
>In case you want to do something only on one rank specifically, you can do that by:
``` {python}
if rank == 0:
    print("Hello World")
```
{: .callout}

Pushing the implementation further, the list of `partitions` needs to be established similar to what was done in the parallel implementation above. Also a list for the results is created and all items are initialized to `0`.

~~~
if rank == 0:
    partitions = [ int(n_samples/size) for item in range(size)]
    counts = [ int(0) ] *size
else:
    partitions = None
    counts = None
~~~
{: .python}

In this example, you can see how the lists are only created on one rank for now (rank `0` to be precise). At this, point the contents of `partitions` and `counts` reside on rank `0` only. They now have to send to all other participanting ranks.

~~~
partition_item = comm.scatter(partitions, root=0)
count_item = comm.scatter(counts, root=0)
~~~
{: .python}

Note how the input variable is `partitions` (aka a list of values) and the output variable is named `partition_item`. This is because, `mpi4py` returns only one item (namely the one item in `partitions` matching the rank of the current process, i.e. `partitions[rank]`) rather than the full list. Now, the actual work can be done.

~~~
count_item = inside_circle(partition_item)
~~~
{: .python}

This is the known function call from the serial implementation. After this, the results have to be communicated back again.

~~~
counts = comm.gather(count_item, root=0)
~~~
{: .python}

The logic from above is reverted now. A single item is used as input, aka `count_item`, and the result `counts` is a list again. In order to compute pi from this, the following operations should be restricted to `rank=0` in order to minimize redundant operations:

~~~
if rank == 0:
    my_pi = 4.0 * sum(counts) / sum(partitions)
~~~
{: .python}

And that's it. Now, Lola can submit her first MPI job.

~~~
$ bsub -n48 -o mpi_numpi.out -e mpi_numpi.err time mpirun python3 ./mpi_numpi.py 1000000000
~~~
{: .bash}

The output file `mpi_numpi.out` yields the following lines:

~~~
[     mpi version] required memory 11444.092 MB
[using  48 cores ] pi is 3.141679 from 1000000000 samples

real    0m6.368s
user    0m45.763s
sys     0m6.681s
~~~
{: .output}

Note here, that we are now free to scale this application to hundreds of core if we want to. We are only restricted by the size of our compute cluster. Before finishing the day, Lola looks at the runtime that here MPI job consumed. `6.4` seconds for a job that ran on twice as much cores as here parallel implementation. That is quite an achievement of the day!

> ## Use the batch system!
>
> Launch the serial and parallel version of the pi_estimate using the batch system. 
> 
{: .challenge}
