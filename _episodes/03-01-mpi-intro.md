---
title: "Parallel Execution"
teaching: 15
exercises: 10
questions:
- "How do I execute a compute job that uses multiple nodes at once?"
- "How do I analyze multiple large files on a cluster the best way?"
objectives:
- "Explain how message passing allows performing computations in more than 1 computer at the same time."
- "Observe the effects of parallel execution of commands with a simple hostname call."
- "Perform a Map-Reduce style operation to extract information from large files and collect these into one final answer."
key points:
- "The mpi driver `mpirun` sends compute jobs to a set of allocated computers."
- "The mpi software then executes these jobs on the remote hosts and synchronizes their state/memory."
- "The `print_hostname.py` infers the hostname of the current machine. If run in parallel with `mpirun`, it prints several different hostnames."
---

Lola Lazy is now confident enough to work with the batch system of the cluster. She now turns her attention to the problem at hand, i.e. estimating the value of _Pi_ to very high precision. 

One of her more experienced colleagues has suggested to her, to use the _Message Passing Interface_ (in short _MPI_) for that matter. As she has no prior knowledge in the field, accepting this advice is as good as trying some other technique on her how. She first explores the documentation of MPI a bit to get a feeling about the philosophy behind this approach. 

> ## Message Passing Interface
> A long time before we had smart phones, tablets or laptops, [compute clusters](http://www.phy.duke.edu/~rgb/brahma/Resources/beowulf/papers/ICPP95/icpp95.html) were already around and consisted of interconnected computers that had merely enough memory to show the first two frames of a movie (`2*1920*1080*4 Bytes = 16 MB`). 
> However, scientific problems back than were equally demanding more and more memory than today. 
> To overcome the lack of available hardware memory, [specialists from academia and industry](https://en.wikipedia.org/wiki/Message_Passing_Interface#History) came about with the idea to consider the memory of several interconnected compute nodes as one. Given a standardized software that synchronizes the various states of memory between the client/slave nodes during the execution of driver application through the network interfaces. With this performing large calculations that required more memory than each individual cluster node can offer was possible. Moreover, this technique by passing messages (hence _Message Passing Interface_ or _MPI_) on memory updates in a controlled fashion allowed to write parallel programs that were capable of running on a diverse set of cluster architectures.

![Schematic View of a Compute Cluster with 4 nodes (12 cores each)](../tikz/cluster_schematic.svg)

Lola becomes curious. She wants to experiment with this parallelisation technique a bit. For this, she would like to print the name of the node where a specific driver application is run. 

~~~
$ bsub -n 4 -o call_hostname.out -e call_hostname.err mpirun hostname
~~~
{: .bash}

The log file that is filled by the `bsub` command, contains the following lines after finishing the job:

~~~
n01
n01
n01
n01
~~~
{: .output}

The output makes her wonder. Apparently, the command was cloned and executed on the same host 4 times. If she increases the number of processors to a number larger than the number of CPU cores each of here nodes has, this might change and the distributed nature of `mpirun` will reveal itself.

~~~
$ bsub -n 16 -o call_hostname.out -e call_hostname.err mpirun hostname
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

![Execution of `mpirun hostname` on a Compute Cluster with 4 nodes (12 cores each)](../tikz/mpirunhostname_on_clusterschematic.svg)

As the figure above shows, 12 instances of `hostname` were called on `n01` and 4 more on `n02`. Strange though, that the last 5 lines are not ordered correctly. Upon showing this result to her colleaque, the latter explains: even though, the `hostname` command is run in parallel across the 2 nodes that are used here, the output of her 16 `hostname` calls need to be merged into one output file (that she called `call_hostname.out`) at the end. This synchronization performed by the `mpirun` application is not guaranteed to happen in an ordered fashion (how could it be as the commands were issued in parallel). Her colleaque explains, that the `hostname` application itself is not aware of _MPI_ in a way that it is not parallelized with it. Thus, the `mpirun` driver simply accesses the nodes that it is allowed to run on by the batch system and launches the `hostname` app. After that, `mpirun` collects the output of the executed commands at completion and writes it to the defined output file `call_hostname.out`.

Like a reflex, Lola asks how to write these MPI programs. Her colleague points out that she needs to program the languages that MPI supports, such as Fortran, C, C++, python and many more. As Lola is most confident with python, her colleague wants to give her a head start using `mpi4py` and provides a minimal example. This example is analogous to what Lola just played with. This python script called `print_hostname.py` prints the number of the current MPI rank (i.e. the unique id of the execution thread within one mpirun invocation), the total number of MPI ranks available and the hostname this rank is currently run on.

~~~
$ bsub -n 16 -o call_hostname.out -e call_hostname.err mpirun python3 print_hostname.py
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

Again, the unordered output is visible. Now, the relation between the rank and the parameters `-n` to bsub becomes more clear. `-n` defines how many processors the current invocation of mpirun requires. If `-n 16` is defined, the rank can run from `0` to `15`.

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
