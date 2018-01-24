---
title: "Bonus session: Distributing computations among computers"
teaching: 45
exercises: 10
questions:
- "What issued the message passing interface (MPI)?"
- "How do I exploit parallelism using the message passing interface (MPI)?"
objectives:
- "Explain how message passing allows performing computations in more than 1 computer at the same time."
- "Observe the effects of parallel execution of commands with a simple hostname call."
- "Measure the run time of parallel and MPI version of the implementation."
keypoints:
- "The MPI driver `mpirun` sends compute jobs to a set of allocated computers."
- "The MPI software then executes these jobs on the remote hosts and synchronizes their state/memory."
- "The `print_hostname.py` infers the hostname of the current machine. If run in parallel with `mpirun`, it prints several different host names."
- "MPI can be used to split the random sampling into components and have several nodes generate random numbers and report back only the pi estimate of this partition."
---

Lola Lazy is now confident enough to work with the batch system of the cluster. She now turns her attention to the problem at hand, i.e. estimating the value of _Pi_ to very high precision. 

One of her more experienced colleagues has suggested to her, to use the _Message Passing Interface_ (in short: _MPI_) for that matter. As she has no prior knowledge in the field, accepting this advice is as good as trying some other technique on her how. She first explores the documentation of MPI a bit to get a feeling about the philosophy behind this approach. 

> ## Message Passing Interface
> A long time before we had smart phones, tablets or laptops, [compute clusters](http://www.phy.duke.edu/~rgb/brahma/Resources/beowulf/papers/ICPP95/icpp95.html) were already around and consisted of interconnected computers that had merely enough memory to show the first two frames of a movie (`2*1920*1080*4 Bytes = 16 MB`). 
> However, scientific problems back than were equally demanding more and more memory than today. 
> To overcome the lack of available hardware memory, [specialists from academia and industry](https://en.wikipedia.org/wiki/Message_Passing_Interface#History) came about with the idea to consider the memory of several interconnected compute nodes as one. Given a standardized software that synchronizes the various states of memory between the client/slave nodes during the execution of driver application through the network interfaces. With this performing large calculations that required more memory than each individual cluster node can offer was possible. Moreover, this technique by passing messages (hence _Message Passing Interface_ or _MPI_) on memory updates in a controlled fashion allowed to write parallel programs that were capable of running on a diverse set of cluster architectures.

![Schematic View of a Compute Cluster with 4 nodes (12 cores each)]({{ page.root }}/tikz/cluster_schematic.svg)

Lola becomes curious. She wants to experiment with this parallelization technique a bit. For this, she would like to print the name of the node where a specific driver application is run. 

~~~
{% include /snippets/03/submit_4_mpirun_hostname.{{ site.workshop_scheduler }} %}
~~~
{: .bash}

The log file that is filled by the command above, contains the following lines after finishing the job:

~~~
n01
n01
n01
n01
~~~
{: .output}

The output makes her wonder. Apparently, the command was cloned and executed on the same host 4 times. If she increases the number of processors to a number larger than the number of CPU cores each of here nodes has, this might change and the distributed nature of `mpirun` will reveal itself.

~~~
{% include /snippets/03/submit_16_mpirun_hostname.{{ site.workshop_scheduler }} %}
~~~
{: .bash}

~~~
n01
n01
n01
n01
n01
n01
n01
n01
n01
n01
n01
n02
n01
n02
n02
n02
~~~
{: .output}

![Execution of `mpirun hostname` on a Compute Cluster with 4 nodes (12 cores each)]({{ page.root }}/tikz/mpirunhostname_on_clusterschematic.svg)

As the figure above shows, 12 instances of `hostname` were called on `n01` and 4 more on `n02`. Strange though, that the last 5 lines are not ordered correctly. Upon showing this result to her colleague, the latter explains: even though, the `hostname` command is run in parallel across the 2 nodes that are used here, the output of her 16 `hostname` calls need to be merged into one output file (that she called `call_hostname.out`) at the end. This synchronization performed by the `mpirun` application is not guaranteed to happen in an ordered fashion (how could it be as the commands were issued in parallel). Her colleague explains, that the `hostname` application itself is not aware of _MPI_ in a way that it is not parallelized with it. Thus, the `mpirun` driver simply accesses the nodes that it is allowed to run on by the batch system and launches the `hostname` app. After that, `mpirun` collects the output of the executed commands at completion and writes it to the defined output file `call_hostname.out`.

Like a reflex, Lola asks how to write these MPI programs. Her colleague points out that she needs to program the languages that MPI supports, such as FORTRAN, C, C++, python and many more. As Lola is most confident with python, her colleague wants to give her a head start using `mpi4py` and provides a minimal example. This example is analogous to what Lola just played with. This python script called [`print_hostname.py`]({{ page.root }}/code/03_parallel_jobs/print_hostname.py) prints the number of the current MPI rank (i.e. the unique id of the execution thread within one mpirun invocation), the total number of MPI ranks available and the hostname this rank is currently run on.

~~~
{% include /snippets/03/submit_16_mpirun_python3_print_hostname.{{ site.workshop_scheduler }} %}
~~~
{: .bash}

~~~
this is 16/16 running on n02
this is 15/16 running on n02
this is 13/16 running on n02
this is 14/16 running on n02
this is  3/16 running on n01
this is  5/16 running on n01
this is 11/16 running on n01
this is  1/16 running on n01
this is  7/16 running on n01
this is  2/16 running on n01
this is  4/16 running on n01
this is  6/16 running on n01
this is  8/16 running on n01
this is  9/16 running on n01
this is 10/16 running on n01
this is 12/16 running on n01
~~~
{: .output}

Again, the unordered output is visible. Now, the relation between the rank and the parameters `-n` to submit command becomes more clear. `-n` defines how many processors the current invocation of mpirun requires. If `-n 16` is defined, the rank can run from `0` to `15`.

> ## Does `mpirun` really execute commands in parallel?
>
> Launch the command `date` 16 times across your cluster. What do you observe? Play around with the precision of date through its flags (`+%N` for example) and study the distribution of the results.  
> 
{: .challenge}

> ## Upgrade `print_hostname.py` and print the time-of-day as well
>
> Open the `print_hostname.py` script with your editor and use the python3 `datetime` module to print the time of day next to the host name and rank number.
> 
{: .challenge}

To finalize this day's work, Lola wants to tackle distributed memory parallelization using the Message Passing Interface (MPI). For this, she uses the `mpi4py` library that is pre-installed on her cluster. She again starts from the [serial implementation]({{ page.root }}/code/03_parallel_jobs/serial_numpi.py). At first, she expands the include statements a bit. 

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
~~~
if rank == 0:
    print("Hello World")
~~~
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

In this example, you can see how the lists are only created on one rank for now (rank `0` to be precise). At this, point the contents of `partitions` and `counts` reside on rank `0` only. They now have to send to all other participating ranks.

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
{% include /snippets/03/submit_48_mpirun_python3_mpi_numpi.{{ site.workshop_scheduler }} %}
~~~
{: .bash}

The output file `mpi_numpi.out` yields the following lines:

~~~
[     mpi version] required memory 11444.092 MB
[using  48 cores ] pi is 3.141679 from 1000000000 samples

real    0m6.546s
user    0m36.436s
sys     0m8.445s
~~~
{: .output}

Note here, that we are now free to scale this application to hundreds of cores if we wanted to. We are only restricted by the size of our compute cluster. Before finishing the day, Lola looks at the run time that her MPI job consumed. `6.5` seconds for a job that ran on four times as much cores as here parallel implementation before (which took `12s` for the same configuration). That is quite an achievement of the day!

> ## Use the batch system!
>
> Launch the serial and parallel version of the pi_estimate using the batch system. 
> 
{: .challenge}

> ## Don't Stress the Network
>
> The MPI implementation given above transmits only the pi estimate per rank to the main program. Rewrite the program so that each rank generates the random numbers and sends them back to rank 0. 
> 
> Submit the job and look at the time it took. What do you observe? Why did the run time change?
{: .challenge}
