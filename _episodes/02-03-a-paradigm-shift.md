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

Another day, Lola discovers a library named `dask` (see more details [here](https://docs.dask.org/en/latest/)) that not only promises high performance, but also appears to be on par with the numpy library, so that she has to apply only minimal changes to the code.

~~~
{% include code/02_parallel_jobs/dask_numpi.py %}
~~~
{: .python}

This [implementation]({{page.root}}/code/02_parallel_jobs/dask_numpi.py) can now be put to work. At this point, a paradigm shift has been introduced silently. Lola's office mate makes her aware of this. It is a subtle change compared to using the `multiprocessing` library, but it is there. 

In this example, the containers for the random numbers have become smart. This is only visible by good measure of the `chunks=-1` argument to the `da.random.uniform` function. A flat container used to just hold numbers in memory wouldn't have to be responsible for the chunking of the data. But dask offers us a container that does so.

Behind the courtains, the dask framework connects containers (`da.array` here) with functions (`operator*`, `operator+`, `da.sqrt`, `da.where`). The framework then infers which functions can act on which data independently. From this, the dask library can complete the program to any degree of parallelism that is needed. 

All this automation comes at a price. The dask implementation is about 2x slower than the pure `multiprocessing` one. But there must be something, we have gained.
