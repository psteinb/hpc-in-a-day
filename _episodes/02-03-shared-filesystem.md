---
title: "Working with the shared file system"
teaching: 25
exercises: 5
questions:
- "How do I store a file on node so that another node can see it?"
- "How do I store a file on node so that another node cannot see it?"
- "Do I really need scp for all of the above?"
objectives:
- "Submit a job that fills a file with arbitrary but known data and store it in the shared file system."
- "Submit a job that fills a file with arbitrary but known data and store it in the local file system of the execution host."
- "Raise the attention that a common file system also makes big problems common to all users very quickly."
keypoints:
- "A shared file system is one of the key components of modern HPC clusters."
- "`scp` and friends are rarely needed on a HPC cluster."
- "A shared file system is a resource for all users, so use it wisely to not affect others."
---

After all these first attempts to make use of the cluster, Lola wonders about something. If she submits a job, how would she be able to store data and access it from her laptop?

Lola comes up with a small example job, that collects information on the node that the jobs is run on and submits it.

~~~
{% include /snippets/02/submit_node_info.{{ site.workshop_scheduler }} %}
~~~
{: .bash }

> ## What's the fuzz about < and > ?
> 
> On the unix command line, the symbols '<' and '>' have a special meaning. They are called output redirection operators. 
>
> `>` takes the output it receives from the left-hand side and stores it into, e.g. a file, on its right-hand side. For example, `date > date.log` stores the output of the date command and stores it inside a file called date.log. 
> 
> `<` takes the content of it's right-hand side, e.g. typically a file, and it provides it as the *input* of the command listed on the left-hand side. `wc < /proc/cpuinfo` takes in the contents of the file `/proc/cpuinfo` and uses it as the input to the wc command (which performs a word count and prints the result).
{: .callout }

When the job is done, Lola scans the current directory from where she submitted the job. But the file that she expects does not appear. Lola goes back to the script she wrote. There is one line that looks suspicious.

~~~
FILENAME=/tmp/`hostname`_info.log
~~~
{: .bash }

She checks the contents of `/tmp`. Nothing as well. That means that where ever Lola's script runs, the output is stored under `/tmp/` but not on the node where she submitted her job from. The problem is that this directory is local to the node where the script is run. There is no automated synchronization, so the file will never appear on the machine where Lola is currently working.

> ## `/tmp`
> This is the standard Linux temporary directory where anyone (i.e. the operating system as well as any user or user application) is allowed to create, write, read and delete files and directories. The directory is typically cleared of any content when the computer is rebooted.
{: .callout }

Lola asks her colleague how to proceed. He mentions that `{{ site.workshop_shared_fast_filesystem }}` is a directory that is a shared file system. In other words any directory under `{{ site.workshop_shared_fast_filesystem }}` is updated in real-time across the entire cluster. As the name suggests, this file system appears to be a very fast one. Her colleague notes it's a parallel file system.

> ## parallel file system
>
> Parallel file systems such as, [lustre](http://lustre.org/), [GPFS](https://www.ibm.com/support/knowledgecenter/en/SSFKCN/gpfs_welcome.html), [BeeGFS](http://www.beegfs.com/content/) etc, are the limbs of a multi-purpose HPC cluster. These file systems consist of a software layer that needs to be installed on all nodes of a cluster and dedicated hardware external to the compute nodes. The mere goal of these systems is to provide high bandwidth for writing and reading large files in parallel, i.e. from multiple nodes at the same time. If it wouldn't be for them, simulations and data analysis jobs would have nowhere to put their results or read their inputs from.

Lola doesn't bother with the technical details for a moment. She simply wants to get the job done. So she changes the offending line to:

~~~
FILENAME={{ site.workshop_shared_fast_filesystem }}/lola/`hostname`_info.log
~~~
{: .bash }

and submits the job. And voila, the file appears in `{{ site.workshop_shared_fast_filesystem }}/lola/` with the expected input: 

~~~
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 45
model name      : Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz
# ...
~~~
{: .output }

Lola is happy. Before leaving, her colleague briefs her, that she should be cautious with this file system. Even though it appears so powerful, misusing it will effects on all other users as it is a **shared** file system.

> ## Space left on device(s)
>
> Use the `df` utility to infer how much space you have left on the current device and on the remote machine. What sizes do you see?
> To check, do:
>
> ~~~~~
> $ df -h
> ~~~~~
{: .challenge}

> ## Multiple times your laptop
>
> Use the `df` utility to infer how much space is available on the largest shared file system on your cluster. Find out how much hard drive space your laptop has. Calculate how many laptop hard drives would fit inside the shared file system on your cluster.
{: .challenge}

> ## What is shared?
>
> Is there any way to know which parts of the folder structure are shared? The answer to this is yes. Explore the following output with your neighbor:
>
> ~~~~~
> $ df
> Filesystem                                        1K-blocks         Used     Available Use% Mounted on
> /dev/sda1                                          30832636      8001936      21241452  28% /
> devtmpfs                                          131950944            0     131950944   0% /dev
> tmpfs                                             131957544      2137112     129820432   2% /dev/shm
> tmpfs                                             131957544       820720     131136824   1% /run
> tmpfs                                             131957544            0     131957544   0% /sys/fs/cgroup
> /dev/sda2                                         429876216        83424     407933312   1% /tmp
> mack1:/home                                       904599936     52544000     852055936   6% /home
> 172.17.254.41@o2ib:172.17.254.42@o2ib:/lustre 2247511864704 538153008184 1686874889292  25% /lustre
> tmpfs                                              26391512            0      26391512   0% /run/user/8900
> ~~~~~
>
> Hint: Recall the syntax for using `ssh`.
>
> > ## Solution
> > The directories `home` and `lustre` (last column) are related to file systems that look like DNS lookup names as you would use for `ssh`. For example, `mack:/home` looks like something you could supply to `scp` as well.
> {: .solution}
{: .challenge}
