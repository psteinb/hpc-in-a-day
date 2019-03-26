---
title: "Searching for Pi"
teaching: 30
exercises: 15
questions:
- "How do I analyze a lot of large files efficiently?"
objectives:
- "Perform a Map-Reduce style operation to extract information from large files and collect these into one final answer."
- "Use applications from 2 programming languages and imitate high-throughput compute."
keypoints:
- "Searching through a large file is bound by the speed that it can be read-in."
- "Having a set of files, the result of searching one file is independent of searching its sibling."
- "HPC clusters have very powerful parallel file systems, that offer the best speed if data is accessed in parallel."
- "The operation of searching through a file can be mapped to individual nodes on the cluster. (map step)"
- "After the map step has been completed, all sub-results have to be reduced to one final result. (reduce step)"
---

Lola comes to work the next day and finds that someone has tempered with her files. Her home directory on the cluster looks like a someone threw dices with the characters of here file names. 

~~~
$ ls
~~~
{: .bash}

~~~
pi_estimate_01.data  pi_estimate_04.data  pi_estimate_07.data  pi_estimate_10.data  pi_estimate_13.data  pi_estimate_16.data
pi_estimate_02.data  pi_estimate_05.data  pi_estimate_08.data  pi_estimate_11.data  pi_estimate_14.data
pi_estimate_03.data  pi_estimate_06.data  pi_estimate_09.data  pi_estimate_12.data  pi_estimate_15.data
~~~
{: .output}

Examining the files shows, that their size has been increased by some orders of magnitude in size. She opens one of her files and finds out that the results are still there, but they are scrambled with random symbols that she never saw before. Certainly, nothing human readable. But she notices that the pi estimates are always printed on an isolated line. This is something she can exploit to extract these lines. She immediately sits down and writes a [simple program]({{ page.root }}/code/03_parallel_jobs/count_pi_estimates.py) to count the number of occurrences of pi along the lines of:

~~~
import sys

if __name__=='__main__':

    current_file = open(sys.argv[1])
    current_file_content = current_file.read()
    count = 0
    for line in current_file_content:
        if line.startswith("3.1"):
            count += 1
    
    print(count)

~~~
{: .python}

She launches the application and waits for quite a while until the she receives an answer (1 minute in this case). She thinks that this is strange. Looking through a some lines of text and checking if a line starts with `3.1` doesn't sound complicated, so why is it taking so long. She expected to get an answer back instantly. Given that she has 16 of these files, if she wants to look through all of them, this means that she has to wait at least 16 minutes for the answer to come along.

Lola wonders, but what do we have a cluster for then? She decides to submit 16 jobs that filter out the estimates of pi for each file. She sits down and alters her previous program to [filter-out the occurrences of pi]({{ page.root }}/code/03_parallel_jobs/filter_pi_estimates.py). The idea of her code is the following:

~~~
import sys

if __name__=='__main__':

    current_file = open(sys.argv[1])
    current_file_content = current_file.read()

    for line in current_file_content:
        if line.startswith("3.1"):
            print(line)
            
~~~
{: .python}

She tests her python program on a single input file. As she knows how long it'll take approximately, she can provide a good estimate of the run time of the job. If the cluster is busy, that allows the scheduler to start her job faster.

~~~
{% include /snippets/03/submit_filter_pi.{{ site.workshop_scheduler }} %}
~~~
{: .bash}

~~~
3.142096
3.141306
3.140558
3.142311
3.141864
3.141112
3.142655
3.140714
~~~
{: .output}

> ## The `bash` can do that too
>
> Filtering out any lines starting with `3.1` can be done with pure bash commands as well.
> 
> ~~~~~
> $ egrep "^3.1" pi_estimate_01.data
> ~~~~~
> {: .bash}
>
> ~~~~~
> 3.142096
> 3.141306
> 3.140558
> 3.142311
> 3.141864
> 3.141112
> 3.142655
> 3.140714
> ~~~~~
> {: .output}

That went pretty well. She is reminded of the map-reduce idiom that she encountered yesterday. That was the map-step that filters out the occurrences she was interested in. She now needs a reduce step to combine all of these estimates to a global one. If she has all of this, she is basically done recovering her work of yesterday. The [code she comes up with]({{ page.root }}/code/03_parallel_jobs/average_pi_estimates.py) is based on her previous programs. 

~~~
import sys

if __name__=='__main__':

    files = sys.argv[1:]
    pi_estimates = []    
    
    for f in files:
        if os.path.exists(f):

            current_file = open(f)
            current_file_content = current_file.read().split("\n")

            for line in current_file_content:
                if line.startswith("3.1"):
                    pi_estimates.append(float(line))
                    
    n_samples = len(pi_estimates)
    print("pi estimates from %i estimates : %f" % (n_samples,sum(pi_estimates)/n_samples))
            
~~~
{: .python}

The question is, she would love to send this averaging job after she filtered everything out. That means, the averaging depends on the filter step. This can be done with the scheduler she has as:


~~~
{% include /snippets/03/map_filter_pi.{{ site.workshop_scheduler }} %}
~~~
{: .bash}

The above is called an _array job_. The same commands are executed on an array of files which share a similar file name. In this case, it is `pi_estimate_01.data, pi_estimate_02.data, pi_estimate_03.data, ...`. When the job runs on the cluster, the shell variable 

~~~
{% include /snippets/03/array_job_task_id.{{ site.workshop_scheduler }} %}
~~~
{: .bash}

is replaced by a number within the interval `[1-16]`. This way, we receive 16 output files that contain the estimates of Pi we are after. Now that this is done, all the estimates in the output files have to be averaged to provide the final result. As the produced files are only kilo-bytes in size, this can be done without the scheduler.

~~~
$ python3 average_pi_estimates.py map_step.1.log map_step.2.log map_step.3.log map_step.4.log 
~~~
{: .bash}

It's tedious to type in all the 16 file names. Lola asks an admin for help that has been using the terminal for quite a while. He mentions the wild card character to use.

~~~
$ python3 average_pi_estimates.py map_step.*.log
~~~
{: .bash}

~~~
averaged value of pi from 224 estimates : 3.141337
~~~
{: .output}

> ## Occurance of 2
>
> Dublicate the steps outlined in this section. Before doing the reduce step, filter out only those estimates of pi that end on an even number. For example, `3.141337` ends on `7` and would be discarded. `3.141332` ends on `2` and hence would be used for the grand average.
>
{: .challenge}

> ## Dependencies
>
> Open the man page(s) of your job scheduler. Search for ways to make the reduce job wait for the map job.
>
{: .challenge}
