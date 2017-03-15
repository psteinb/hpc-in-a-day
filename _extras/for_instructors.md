# Instructor's Briefung

This document tries to describe what preparations are required of instructors to make the workshop work as smooth as possible. 

## Chapter 1

## Chapter 2

## Chapter 3

### Section 3, Searching for Pi

Use the file [generate_scrambled_data.py](./code/03_parallel_jobs/generate_scrambled_data.py) to produce 16 files that comply to the files used in this section, e.g. : 

```
pi_estimate_01.data  pi_estimate_04.data  pi_estimate_07.data  pi_estimate_10.data  pi_estimate_13.data  pi_estimate_16.data
pi_estimate_02.data  pi_estimate_05.data  pi_estimate_08.data  pi_estimate_11.data  pi_estimate_14.data
pi_estimate_03.data  pi_estimate_06.data  pi_estimate_09.data  pi_estimate_12.data  pi_estimate_15.data
```
{: .output}

This could be done like so:

~~~
$ for i in `seq -f "%02.0f" 1 16`;do python3 ./generate_scrambled_data.py pi_estimate_${i}.data;done
~~~
{: .output}

At best, create directories for the each learner so that they don't get into each other's way.

Note, that this lesson is currently quite fragile as the i/o caching can easily get into the way of the learners. 
