---
title: "Working with the scheduler"
teaching: 25
exercises: 5
questions:
- "How do I know if something went wrong?"
- "How to decrease the waiting time of your job?"
- "How do I cancel a job?"
objectives:
- ""
key points:
- "n.n."
---

While submitting more tests jobs, Lola observes that she always mirrors the current directory for a log file to appear. This sometimes takes awhile and sometimes this happens almost instantly. How does she know, if a job is running or not?

{% highlight bash %}
{% include /snippets/02/submit_hostname_date_sleep.{{ site.workshop_scheduler }} %}
{% endhighlight %}

Now Lola tries one of the monitoring commands, the she discovered in the manpages of her scheduler:

{% highlight bash %}
{% include /snippets/02/monitor_hostname_date_sleep.{{ site.workshop_scheduler }} %}
{% endhighlight %}

{% highlight bash %}
{% include /snippets/02/output_monitor_hostname_date_sleep.{{ site.workshop_scheduler }} %}
{% endhighlight %}

The output of the monitoring command provides her some telemetry data of her job: 

- in what state is her job (waiting to start also known as 'pending', is running, is it failing)
- on what node is her job running 
- where did she submit the job to
- the time she submitted the job
- the job name

All of these information might appear pointless when submitting only one job at a time. But in larger data analysis or simulation campaigns, when individual users submit hundreds or thousands of jobs, these information become crucial. 

Lola is quite happy with her progress so far. All of a sudden, she detects a mistake in one of her scripts. 

{% highlight bash %}
{% include /snippets/02/submit_hostname_date_sleep300.{{ site.workshop_scheduler }} %}
{% endhighlight %}

No, that shouldn't happen! She doesn't want to wait 5 minutes for the job to complete. So Lola would love to cancel this job. 

{% highlight bash %}
{% include /snippets/02/find_hostname_date_sleep300.{{ site.workshop_scheduler }} %}
{% endhighlight %}

For this, she needs to find job ID of the job that she would like to stop. With this, she can ask the scheduler to cancel her job.

{% highlight bash %}
{% include /snippets/02/kill_hostname_date_sleep300.{{ site.workshop_scheduler }} %}
{% endhighlight %}

Right before lunch on that day, Lola notices that more and more staff members of her lab start using the cluster. Her own jobs that she would like to have done before lunch tend to wait for longer than expected before they are actually started. Lola revisits the cluster documentation. Maybe she oversaw something there? She finds a passage that talks about the possibility to provide the scheduler the estimated runtime of her job (sometimes also referred to as _walltime_).


