---
title: "Parallel Estimation of Pi for Pedestrians"
teaching: 30
exercises: 15
questions:
- "What are data parallel algorithms?"
- "How can I estimate the yield of parallelization without writing one line of code?"
- "How do I use multiple cores on a computer in my program?"
objectives:
- "Use the profiling data to calculate the theoretical speed-up."
- "Use the theoretical speed-up to decide for an implementation."
- "Use the multiprocessing module to create a pool of workers."
- "Let each worker have a task and improve the runtime of the code as the workers can work independent of each other."
- "Measure the run time of both the parallel version of the implementation and compare it to the serial one."
keypoints:
- "Amdahl's law is a description of what you can expect of your parallelisation efforts."
- "Use the profiling data to calculate the time consumption of hot spots in the code."
- "The generation and processing of random numbers can be parallelized as it is a data parallel task."
- "Time consumption of a single application can be measured using the `time` utility."
- "The ratio of the run time of a parallel program divided by the time of the equivalent serial implementation, is called speed-up."
---

> ## Parallel for real 1
>
> What of the following is a task, that can be parallelized in real life:
> 
> 1. Manually copying a book and producing a clone 
> 2. Clearing the table after dinner
> 3. Rinsing the dishes 
> 4. A family getting dressed to leave the appartment for birthday party
>
> > ## Solution
> > 1. not parallel as we have to start with one book and only have one reader/writer
> > 2. parallel, the more people help, the better
> > 3. not parallel, as we typically only have one sink
> > 4. parallel, each family member can get dressed independent of each other 
> {: .solution}
{: .challenge}

> ## Parallel for real 2
>
> What of the following is a task, that can be parallelized in real life:
> 
> 1. Compressing the contents of a directory full of files
> 2. Converting the currency of rows in a column of a large spreadsheet (10 million rows)
> 3. Writing an e-mail in an online editor
> 4. Playing a Video on youtube/vimeo/etc. or in a video player application
>
> > ## Solution
> > 1. parallel, each file can be compressed seperately
> > 2. parallel, each row can be converted seperately
> > 3. not parallel, we only have one writer (you)
> > 4. not parallel, you only have one consumer (you), rendering the movie in 2 windows in parallel does not help
> {: .solution}
{: .challenge}

Having the profiling data, our estimate of pi is a valuable resource.

~~~~~
$ kernprof-3 -l ./serial_numpi_annotated.py 50000000
[serial version] required memory 572.205 MB
[serial version] pi is 3.141728 from 50000000 samples
Wrote profile results to serial_numpi_annotated.py.lprof
$ python3 -m line_profiler serial_numpi_profiled.py.lprof
Timer unit: 1e-06 s

Total time: 2.04205 s
File: ./serial_numpi_profiled.py
Function: inside_circle at line 7

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     7                                           @profile
     8                                           def inside_circle(total_count):
     9                                           
    10         1       749408 749408.0     36.7      x = np.float32(np.random.uniform(size=total_count))
    11         1       743129 743129.0     36.4      y = np.float32(np.random.uniform(size=total_count))
    12                                           
    13         1       261149 261149.0     12.8      radii = np.sqrt(x*x + y*y)
    14                                           
    15         1       195070 195070.0      9.6      filtered = np.where(radii<=1.0)
    16         1        93290  93290.0      4.6      count = len(radii[filtered])
    17                                           
    18         1            2      2.0      0.0      return count
~~~~~

The key points were, that `inside_circle` consumed the majority of the runtime (99%). Even more so, the generation of random numbers consumed the most parts of the runtime (73%). 

More over, the generation of random numbers in x and in y is independent (two seperate lines of code). So there is another way to expliot data independence:

![Illustration of drawing random number pairs `x` and `y` and their dependency with respect to the dimension]({{ page.root }}/tikz/data_coords_parallel_estimate_pi.svg)


> ## Numpy madness
>
> Numpy is a great library for doing numerical computations in python (this where its name originates). In terms of readability however, the numpy syntax does somewhat obscure what is happening under the hood. For example:
>
> ~~~~~
> a = np.random.uniform(size=10)
> b = np.random.uniform(size=10)
> 
> c = a + b
> ~~~~~
> 
> First of, `np.random.uniform(size=10)` creates a list of 10 random numbers. Cross check this by printing it to the terminal. 
>
> Second, `c = a + b` refers to the plus operation performed item by item of the participating arrays or lists. It can be rewritten as:
>
> ~~~~~
> for i in range(len(a)):
>   c[i] = a[i] + b[i]
> ~~~~~
{: .callout}


Another approach is trying to compute as many independent parts as possible in parallel. In this case here, we can make the observation that each pair of numbers in `x` and `y` is independent of each other. 

![Illustration of drawing random number pairs `x` and `y` and their dependency with respect to the pair generated]({{ page.root }}/tikz/data_pairs_parallel_estimate_pi.svg)

This behavior is often referred to as _data parallelism_. 

> ## Data Parallel Code 1
>
> Does this code expose data independence?
> 
> ~~~~~~
> my_data = [ 0, 1, 2, 3, 4, ... ]
>
> for i in range(len(my_data)):
>   my_data[i] = pi*my_data[i]
> ~~~~~~
>
> This code in numpy would be:
>
> ~~~~~
> my_data = np.array([ 0, 1, 2, 3, 4, ... ])
> 
> my_data = pi*my_data
> ~~~~~
{: .challenge}

> ## Data Parallel Code 2
>
> Does this code expose data independence?
> 
> ~~~~~~
> my_data = [ 0, 1, 2, 3, 4, ... ]
>
> for i in range(len(my_data)):
>   if my_data[i] % 2 == 0:
>       my_data[i] = 42
>   else:
>       my_data[i] = 3*my_data[i]
> ~~~~~~
>
> This code in numpy would be:
>
> ~~~~~
> my_data = np.array([ 0, 1, 2, 3, 4, ... ])
> 
> my_data[np.where(my_data % 2 == 0)] = 42
> my_data[np.where(my_data % 2 != 0)] = 3*my_data[np.where(my_data % 2 != 0)]
> ~~~~~
{: .challenge}

> ## Data Parallel Code 3
>
> Does this code expose data independence?
> 
> ~~~~~~
> from random import randint
> my_data = [ 0, 1, 2, 3, 4, ... ]
>
> for i in range(len(my_data)):
>   my_data[i] = 42*my_data[randint(0,len(my_data))]
> ~~~~~~
{: .challenge}

Lola now wonders how to proceed. There are multiple options at her disposal. But given her limited time budget, she thinks that trying them all out is tedious. She discusses this with her office mate over lunch. Her colleaque mentions that this type of consideration was first discussed by Gene Amdahl in 1967 and goes by the name of [Amdahl's law](https://en.wikipedia.org/wiki/Amdahl%27s_law). This law provides a simple of mean of calculating how fast a program can get when parallelized for a fixed problem size. By profiling her code, Lola has all the ingredients to make this calculation. 

The performance improvement of a program, given an original implementation and an improved one is referred as __speed-up S__. Given a program, we can measure the runtime portion of the code that can be benefit from use of more resources (in our case parallel computations), aka __parallel portion p__. For this __parallel portion__, we finally need how much this can be sped-up, which we will refer to as __serial speed-up s__. 

Given all these ingredients, the theoretical speed-up of the whole program is given by:

~~~~~
           1
S = ---------------
    (1 - p) + (p/s)
~~~~~

> ## Independent Coordinates
> 
> Let's take Lola's idea of executing the generation of random numbers per coordinate `x` and `y` from above:
>
> ![Illustration of drawing random number pairs `x` and `y` and their dependency with respect to the dimension]({{ page.root }}/tikz/data_coords_parallel_estimate_pi.svg)
>
> The parallel portion of these two operations amounts to `37+36=73%` of the overall runtime, i.e. `p = 73% = 0.73`. As we want to make the generation of random numbers in x to one task and the generation of random numbers in y to another one, the speed-up `s = 2`.
>
> ~~~~~
>            1                   1          1
> S = -------------------  = --------- = ------- = 1.575
>     1 - 0.73 + (0.73/2)    1 - 0.365    0.635
> ~~~~~
> 
> S for practical matters is at this point just a number. But this can bring us in a position, where we can rate different approaches for their viability to parallelize. 
{: .callout}

> ## Chunking the data
>
> Take Lola's position and compute the theoretical speed up if she would partition the generation of random numbers in 4 parts. In other words, she would rewrite `inside_circle` as:
>
> ~~~~~
> def inside_circle(total_count):
>    
>    count_per_chunk = int(total_count/4)
>    x = np.float32(np.random.uniform(size=count_per_chunk))
>    y = np.float32(np.random.uniform(size=count_per_chunk))
>
>    for i in range(4-1):
>       x = np.append(x,np.float32(np.random.uniform(size=count_per_chunk)))
>       y = np.append(y,np.float32(np.random.uniform(size=count_per_chunk)))
> 
>    radii = np.sqrt(x*x + y*y)
>
>    filtered = np.where(radii<=1.0)
>    count = len(radii[filtered])
>    
>    return count 
> ~~~~~
> 
> For the sake of the example, we assume that the line profile looks identical to the original implementation above. Compute the theoretical speed-up S!
> Which implementation should Lola choose now? 
{: .challenge}

> ## Always go parallel! Right?
>
> Profile this [python application]({{ page.root }}/downloads/volume_pylibs.py) which computes how much disk space your python standard library consumes.
> The algorithm works in 2 steps:
> 1. create list of absolute paths of all `.py` files in your python's system folder
> 2. loop over all paths from 1. and sum up the space on disk each file consumes
>
> Is this a task worth parallelizing? Make a guess!
> Verify your answer using profiling and computing the theoretical speed-up possible.
{: .challenge}


So the bottom line(s) of Amdahl's law are:

- we can speed up a program if we drive `p` as close as possible towards `1`, in other words we should try to parallelize at best the entire program 
- we can speed up a program if we drive `s` to a large number, in other words we should find ways to speed-up portions of the code as best as possible
- there is a limit to the speed-up that we can achieve 

![Comparison of different speed-ups and parallel portions]({{ page.root }}/fig/03/amdahls_law.svg)

> ## Surprise! More limits.
> 
> Until here `s` was of a bit dubious nature. It was a proprerty of the parallel implementation of our code. In practise, this number is not only limited algorithmically, but also by the hardware your code is running on.
>
> Modern computers consist of 3 major parts most of the time:
> - a core processing unit (CPU)
> - some non-persistent memory (RAM)
> - input/output devices
> (we omit disks, network cards, monitors, keyboards, GPUs, etc for the sake of argument)
>
> When a program wants to perform a computation, it most of the time reads in some data, stores it in memory (RAM) and performs computations on it using the CPU. Modern CPUs can do more than one thing at a time, mostly because they consist of more than one "device" than can perform a computation. This "device" is called a CPU core. When we want to perform some tasks in parallel to one another, the amout of work that can be done in parallel is limited by the amount of CPU cores that can perform computations. So, the number of CPU cores is the hard limit for parallelizing any computation. 
{: .callout}

Keeping this in mind, Lola decides to split up the work for multiple cores requires Lola to split up the number of total samples by the number of cores available and calling `count_inside` on each of these partitions:

![Partitioning `x` and `y`]({{ page.root }}/tikz/partition_data_parallel_estimate_pi.svg)

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

![Partitioning `x` and `y` and results of reach partition]({{ page.root }}/tikz/partition_data_parallel_estimate_pi_with_results.svg)

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
    
So from the above, Lola wants to compare the `real` time spent by her serial implementation (`0m12.766`) and compare it to the `real` time spent by her parallel implementation (`0m1.942s`). Apparently, her parallel program was `6.6` times faster than the serial implementation. 

We can compare this to the maximum speed-up that is achievable: `S = 1/(1 - 0.99 + 0.99/12) = 10.8`
That means, our parallel implementation does already a good job, but only achieves `100*6.6/10.8 = 61.1%` runtime improvement of what is possible. As achieving maximum speed-up is hardly ever possible, Lola leaves that as a good end of the day and leaves for home.

> ## Adding up times
> The output of the `time` command is very much bound to how a operating system works. In an ideal world, `user` and `sys` of serial programs should add up to `real`. Typically they never do. The reason is, that the operating systems used in HPC and on laptops or workstations are set up in a way, that the operating system decides which process receives time on the CPU (aka to perform computations). Once a process runs, it may however happen, that the system decides to intervene and have some other binary have a tiny slice of a CPU second while your application is executed. This is where the mismatch for `user+sys` and `real` comes from.
> Note also how the `user` time of the parallel program is a lot larger than the time that was actually consumed. This is because, `time` reports accumulated timings i.e. it adds up CPU seconds that were consumed in parallel.
{: .callout}

> ## Parallel word count
>
> Download [this python script]({{ page.root }}/downloads/count_pylibs.py) to your current directory. Run it by executing:
> 
> ~~~~~
> $ python3 count_pylibs.py
> 4231827 characters and 418812 words found in standard python libs
> ~~~~~
> {: .bash}
> 
> Examine the application if you can find data parallelism. 
{: .challenge}


