---
title: "Higher levels of parallelism"
teaching: 30
exercises: 15
questions:
  - "What were the key changes when using the multiprocessing library?"
  - "How could this be implemented with dask?"
  - "How does a conversion using `dask` high level API compare?"
objectives:
  - "Use a high level description of your algroithm."
  - "Measure the runtime of the dask implementation."
keypoints:
  - "The implementation using multiprocessing used python stdlib components. (very portable)"
  - "The dask library offers parallelisation using constructs that are very numpy like."
  - "To port to dask only the import statements and the container construction needs to be changed."
  - "The advantage of these changes lie in the capability to scale the job to larger machines (test locally, scale globally)."
  - "At the heart of the ease of use lie 'standardized' building blocks for algorithms using the map-reduce paradigm."
  - "Amdahl's law still holds."
---

Lola observes the code she has just written. She asks her room mate if she could review it. So both of them sit down in front of the screen and go through the code again.

~~~
{% include code/02_parallel_jobs/parallel_numpi.py %}
~~~
{: .python}

Lola's office mate observes, that:

- the libraries used are all contained in the python3 standard library   
(anybody else that wants to use this software only needs python3 and nothing else)

- Lola uses implicit parallelisation by using `multiprocessing.Pool`, i.e. she doesn't need to manage her workers/threads/cores in any way

- it's nice that Lola can reuse parts of her serial implementation

- doing the calculation of the partitions looks quite error prone

- larger portions of the code appear dependent on `ncores`

- using `multiprocessing` limits Lola to using only one machine at a time

Lola agrees to these observations and both argue that an alternative implementation using higher level abstractions of the underlying hardware might be a good idea.

Another day, Lola discovers a library named `dask` (see more details [here](https://docs.dask.org/en/latest/)) that not only promises high performance, but also appears to be on par with the numpy library, so that she has to apply only minimal changes to the code. This library can be installed on Lola's cluster by

~~~
$ pip3 install --user dask
~~~
{: .bash}

She now sets out to study the documentation of `dask` and comes up with the following code:

~~~
{% include code/02_parallel_jobs/dask_numpi.py %}
~~~
{: .python}

This [implementation]({{page.root}}/code/02_parallel_jobs/dask_numpi.py) can now be put to work. At this point, a paradigm shift has been introduced silently. Lola's office mate makes her aware of this. It is a subtle change compared to using the `multiprocessing` library, but it is there. 

In this example, the containers for the random numbers have become smart. This is only visible by good measure of the `chunks=-1` argument to the `da.random.uniform` function. A flat container used to just hold numbers in memory wouldn't have to be responsible for the chunking of the data. But dask offers us a container that does so.

Behind the courtains, the dask framework connects containers (`da.array` here) with functions (`operator*`, `operator+`, `da.sqrt`, `da.where`). The framework then infers which functions can act on which data independently. From this, the dask library can complete the program to any degree of parallelism that is needed. 

All this automation comes at a price. The dask implementation is about 2x slower than the pure `multiprocessing` one. But there must be something, Lola has gained. The answer will become evident, when we dive into more details of the `dask` eco system as dask is HPC-ready.

~~~
$ pip3 install --user distributed bokeh
~~~
{: .bash}

When consulting the `dask.distributed` [documentation](https://distributed.dask.org/en/latest/index.html), Lola recognizes that she needs to adopt her code to work with `dask.distributed`.

~~~
{% include code/02_parallel_jobs/distributed.dask_numpi.py %}
~~~
{: .python}

Following the adivce from the [`dask` documentation](https://distributed.dask.org/en/latest/quickstart.html#setup-dask-distributed-the-hard-way), she has to do some manual work first, before she can launch the dask processes.

First, she needs to start the `dask-scheduler`.

~~~
$ dask-scheduler > scheduler.log 2>&1 &
~~~
{: .bash}

~~~
distributed.scheduler - INFO - -----------------------------------------------
distributed.scheduler - INFO - Clear task state
distributed.scheduler - INFO -   Scheduler at: tcp://192.168.178.25:8786
distributed.scheduler - INFO -       bokeh at:                     :8787
distributed.scheduler - INFO - Local Directory: /tmp/user/1000/scheduler-k05cez5y
distributed.scheduler - INFO - -----------------------------------------------
~~~
{: .output}

Then, she starts one workers for testing:

~~~
$ dask-worker 192.168.178.25:8786 > worker.log 2>&1 &
~~~
{: .bash}

Lola notices how she has to connect the 2 processes by an IP address `192.168.178.25:8786`. After doing all of this, she runs [her script]({{page.root}}/code/02_parallel_jobs/distributed.dask_numpi.py) again:

~~~
$ python3 distributed.dask_numpi.py
~~~
{: .bash}

Something has changed. She receives the result much quicker now. Is that reproducible? Lola measures and observes that the runtime of `dask.distributed` is very close to the runtime of the `multiprocessing` implementation.

By chance, she talks to her office mate about this. They discover that there is more waiting for them. She opens the URL at `192.168.178.25:8787` in her browser. Lola is sees an interesting dashboard:

![](fig/dask-dashboard_1024px.png)

In an cluster environment, this is now a powerful feature. Scaling the application has just become manageable. So let's get real and scale across multiple nodes on the cluster. For this, we start the central `dask-scheduler` on the login node. This is a process that only handles network traffic and hence should not (to be monitored) consume too many resources.

~~~
$ dask-scheduler > scheduler.log 2>&1 &
~~~
{: .bash}

Note, we are sending this process into the background immediately and route its output including all errors into `scheduler.log`. The output of this command should look like this (if not, there is a problem):

~~~
distributed.scheduler - INFO - Clear task state
distributed.scheduler - INFO -   Scheduler at:  tcp://1.1.1.42:8786
distributed.scheduler - INFO -       bokeh at:        1.1.1.42:8787
distributed.scheduler - INFO - Local Directory:    /tmp/scheduler-xp31e5sl
distributed.scheduler - INFO - -----------------------------------------------
~~~
{: .output}

Subsequently, we have to start a worker on a cluster node and connect it to the scheduler by means of the IP address:

~~~
$ cat worker.sh
#!/bin/bash
#SBATCH --exclusive
#SBATCH -t 01:00:00
#SBATCH --exclusive

dask-worker tcp://1.1.1.42:8786
$ sbatch -o worker1.log  worker.sh
~~~
{: .bash}

Now, we have to update the address of the scheduler inside our dask python script:

~~~
client = Client("tcp://1.1.1.42:8786")
~~~
{: .python}

As Lola observes, all parts of this dask system are connected by a single point, i.e. the IP address of the `dask-scheduler`. Lola can now run her dask scripts from the node where the `dask-scheduler` was started.

~~~
$ python3 distributed.dask_numpi.py
~~~
{: .bash}

She will notice that the dashboard at `1.1.1.42:8787` is now filled with moving boxes. Her application runs. But, how about adding another node?

~~~
$ sbatch -o worker2.log  worker.sh
~~~
{: .bash}

She is curious if the 2 workers can be used by her code.

~~~
$ python3 distributed.dask_numpi.py
~~~
{: .bash}

Lola smiles while looking at the dashboard. This was after all very easy to setup. She has now reached a precision boundary that no other emplyee has reach for estimating pi.
