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

{% highlight bash %}
{% include /snippets/02/monitor_hostname_date_sleep.{{ site.workshop_scheduler }} %}
{% endhighlight %}
