---
title: "Working with the scheduler"
teaching: 25
exercises: 5
questions:
- "How do I know if something went wrong with my jobs?"
- "How to decrease the waiting time of your jobs?"
- "How do I cancel a job?"
objectives:
- "Submit a job and monitor the status of it."
- "Decipher the output of the monitoring application."
- "Quit or cancel an already running job."
- "Specify the expected runtime of your job to decrease the waiting time."
keypoints:
- "As there are many users logged in, using monitoring tools is key."
- "People commit errors. Cancelling jobs is key to make your admin happy and not stress the system unnecessarily."
- "The more information you give the job scheduler about your job, the quicker it will be dispatched/spooled."
---

While submitting more tests jobs, Lola observes that she always mirrors the current directory for a log file to appear. This sometimes takes awhile and sometimes this happens almost instantly. How does she know, if a job is running or not?

~~~ 
{% include /snippets/02/submit_hostname_date_sleep.{{ site.workshop_scheduler }} %}
~~~
{: .bash}

Now Lola tries one of the monitoring commands, the she discovered in the manpages of her scheduletc/bash_completioner:

~~~
{% include /snippets/02/monitor_hostname_date_sleep.{{ site.workshop_scheduler }} %}
~~~
{: .bash}

~~~
{% include /snippets/02/output_monitor_hostname_date_sleep.{{ site.workshop_scheduler }} %}
~~~
{: .output}


The output of the monitoring command provides her some telemetry data of her job: 

- in what state is her job (waiting to start also known as 'pending', is running, is it failing)
- on what node is her job running 
- where did she submit the job to
- the time she submitted the job
- the job name

All of these information might appear pointless when submitting only one job at a time. But in larger data analysis or simulation campaigns, when individual users submit hundreds or thousands of jobs, these information become crucial. 

Lola is quite happy with her progress so far. All of a sudden, she detects a mistake in one of her scripts. 

~~~
{% include /snippets/02/submit_hostname_date_sleep300.{{ site.workshop_scheduler }} %}
~~~
{: .bash}


No, that shouldn't happen! She doesn't want to wait 5 minutes for the job to complete. So Lola would love to cancel this job. 

~~~
{% include /snippets/02/find_hostname_date_sleep300.{{ site.workshop_scheduler }} %}
~~~
{: .bash}

For this, she needs to find job ID of the job that she would like to stop. With this, she can ask the scheduler to cancel her job.

~~~
{% include /snippets/02/kill_hostname_date_sleep300.{{ site.workshop_scheduler }} %}
~~~
{: .bash}


Right before lunch on that day, Lola notices that more and more staff members of her lab start using the cluster. Her own jobs that she would like to have done before lunch tend to wait for longer than expected before they are actually started. Lola revisits the cluster documentation. Maybe she oversaw something there? She finds a passage that talks about the possibility to provide the scheduler the estimated run time of her job (sometimes also referred to as _wall time_).

> ## Wall time ?
> Wall-clock time, or wall time, is the human perception of the passage of time from the start to the completion of a task. In the context of a task being performed on a computer, wall-clock time is a measure of the real time that elapses from start to end, including time that passes due to programmed (artificial) delays or waiting for resources to become available. In other words, it is the difference between the time at which a task finishes and the time at which the task started. Wall-clock time is the time that a clock on the wall (or a stopwatch in hand) would measure as having elapsed between the start of the process and "now". (from [en.wikipedia.org/wiki/Wall-clock_time](en.wikipedia.org/wiki/Wall-clock_time))
{: .callout}


The documentation indicates that she can provide an estimate of the _wall time_ of her job to the scheduler. 

~~~
{% include /snippets/02/submit_walltime_hostname_date_sleep300.{{ site.workshop_scheduler }} %}
~~~
{: .bash}


As the default wall time limit of the jobs is much higher than 6 minutes, Lola's job is started a lot earlier than the one of her colleagues and she does finish her tasks before she goes to lunch.

> ## errors and outputs
>
> Submit [this script](/snippets/02/errors_and_outputs.sh) to your cluster and split the output in stdout and stderr. Check the contents of the log files that were created. Use the manpage(s) of your scheduler to make the scheduler send both stdout and stderr to the same file.
>
{: .challenge}
